from vkwave.bots.fsm import ANY_STATE
from vkwave.bots import (
    TextFilter,
    StateFilter,
    DefaultRouter,
    BotEvent,
    simple_bot_message_handler,
    FiniteStateMachine,
    State,
    ForWhat,
)


fsm = FiniteStateMachine()
fsm_training_router = DefaultRouter()
# router.registrar.add_default_filter(StateFilter(fsm, ..., ..., always_false=True))
# fsm_training_router.registrar.add_default_filter(StateFilter(fsm, for_what=ForWhat.FOR_USER, always_false=True))


class FSMTraining:
    phone = State("phone")
    name = State("name")
    practice = State("practice")
    work = State("work")
    age = State("age")


#  starting poll
@simple_bot_message_handler(
    fsm_training_router,
    TextFilter('-an'),
)
async def start_fsm_training(event: BotEvent):
    await fsm.set_state(event=event, state=FSMTraining.phone, for_what=ForWhat.FOR_USER)
    return await event.answer("1. Укажите, пожалуйста, ваш контактный номер телефона")


#  exiting from poll (works on any state)
@simple_bot_message_handler(
    fsm_training_router,
    TextFilter('отменить'),
    StateFilter(fsm=fsm, state=ANY_STATE, for_what=ForWhat.FOR_USER),
)
async def exit_fsm_training(event: BotEvent):
    # Check if we have the user in database
    if await fsm.get_data(event, for_what=ForWhat.FOR_USER) is not None:
        await fsm.finish(event=event, for_what=ForWhat.FOR_USER)
    return await event.answer("Спасибо, вы сможете продолжить в любое время")


@simple_bot_message_handler(
    fsm_training_router,
    StateFilter(fsm=fsm, state=FSMTraining.phone, for_what=ForWhat.FOR_USER),
)
async def phone_fsm_training(event: BotEvent):
    await fsm.set_state(
        event=event,
        state=FSMTraining.name,
        for_what=ForWhat.FOR_USER,
        extra_state_data={"phone": event.object.object.message.text},
    )
    return await event.answer("2. Введите ваше имя")


@simple_bot_message_handler(
    fsm_training_router,
    StateFilter(fsm=fsm, state=FSMTraining.name, for_what=ForWhat.FOR_USER),
)
async def name_fsm_training(event: BotEvent):
    await fsm.set_state(
        event=event,
        state=FSMTraining.practice,
        for_what=ForWhat.FOR_USER,
        extra_state_data={"name": event.object.object.message.text},
    )
    return await event.answer("3. Вы уже имеете опыт в наращивании ресниц?")


@simple_bot_message_handler(
    fsm_training_router,
    StateFilter(fsm=fsm, state=FSMTraining.practice, for_what=ForWhat.FOR_USER),
)
async def practice_fsm_training(event: BotEvent):
    await fsm.set_state(
        event=event,
        state=FSMTraining.work,
        for_what=ForWhat.FOR_USER,
        extra_state_data={"practice": event.object.object.message.text},
    )
    return await event.answer("4. Кем вы сейчас работаете или чем занимаетесь? Выберите ниже или напишите свой вариант.")

@simple_bot_message_handler(
    fsm_training_router,
    StateFilter(fsm=fsm, state=FSMTraining.work, for_what=ForWhat.FOR_USER),
)
async def practice_fsm_training(event: BotEvent):
    await fsm.set_state(
        event=event,
        state=FSMTraining.age,
        for_what=ForWhat.FOR_USER,
        extra_state_data={"practice": event.object.object.message.text},
    )
    return await event.answer("5. Укажите ваш возраст, либо пропустите данный пункт.")

@simple_bot_message_handler(
    fsm_training_router,
    StateFilter(fsm=fsm, state=FSMTraining.age, for_what=ForWhat.FOR_USER),
)
async def age_fsm_training(event: BotEvent):
    if not event.object.object.message.text.isdigit():
        return f"Укажите правильное значение, либо пропустите данный пункт, или отмените!"
    await fsm.add_data(
        event=event,
        for_what=ForWhat.FOR_USER,
        state_data={"age": event.object.object.message.text},
    )
    user_data = await fsm.get_data(event=event, for_what=ForWhat.FOR_USER)

    await fsm.finish(event=event, for_what=ForWhat.FOR_USER)
    return f"Your data - {user_data}"
