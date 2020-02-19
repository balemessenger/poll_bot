# In the name of God

from unittest.mock import Mock

from behave import given, when, then

from state_machine.states import States
from controller.start_controller import MainController


@given('a bot and update from server')
def step_impl(context):
    context.bot = Mock()
    context.update = Mock()
    context.dispatcher = Mock()
    context.start_controller = MainController(dispatcher=context.dispatcher)


@when('user send /start')
def step_impl(context):
    context.first_step = context.start_controller.start(context.bot, context.update)


@then('send main menu')
def step_impl(context):
    assert context.first_step == States.MENU
