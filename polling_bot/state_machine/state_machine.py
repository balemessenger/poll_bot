# In the name of God

from telegram.ext import ConversationHandler, CommandHandler, RegexHandler, Filters, MessageHandler, Dispatcher

from ..controller.polling_controller import PollingController
from ..controller.start_controller import MainController
from ..state_machine.states import States
from ..view.constant_messages import Commands, Buttons


class StateMachine:
    def __init__(self, dispatcher: Dispatcher):
        self.dispatcher = dispatcher
        self.polling_handler = PollingController(self.dispatcher)
        self.main_controller = MainController(self.dispatcher)

    def start(self):
        for function_name, function in StateMachine.__dict__.items():
            if callable(function) and function_name.startswith("_set"):
                function(self)

    def _set_start_controller(self):

        conversation_handler = ConversationHandler(
            entry_points=[CommandHandler(command=Commands.start, callback=self.main_controller.main_menu),
                          RegexHandler(pattern=".*",callback=self.main_controller.main_menu)],
            states={},
            allow_reentry=True,
            fallbacks=[]
        )
        register_conversation = ConversationHandler(
            entry_points=[RegexHandler(pattern=Buttons.register,callback=self.registerController.ask_age)],
            states={States.EXPERIENCE_DURATION:[MessageHandler(filters=Filters.text,callback=self.registerController.get_experience_duration)],
                    States.FIELD:[MessageHandler(filters=Filters.text,callback=self.registerController.get_field)],
                    States.FINISH_REGISTER:[MessageHandler(filters=Filters.text,callback=self.registerController.finish_register)]},
            allow_reentry=True,
            fallbacks=[]
        )
        polling_conversation = ConversationHandler(
            entry_points=[RegexHandler(pattern=Buttons.polling, callback=self.polling_handler.ask_question)],
            states={
                States.SHOW_QUESTIONS:[RegexHandler(pattern=Buttons.continue_polling, callback=self.polling_handler.show_questions)],
                States.QUESTION:[MessageHandler(filters=Filters.text,callback=self.polling_handler.show_questions)]
            },
            allow_reentry=True,
            fallbacks=[]
        )
        polling_start_conversation = ConversationHandler(
            entry_points=[RegexHandler(pattern=Buttons.show_polling_questions, callback=self.polling_handler.show_questions)],
            states={
                States.QUESTION: [MessageHandler(filters=Filters.text, callback=self.polling_handler.show_questions)]
            },
            allow_reentry=True,
            fallbacks=[]
        )
        document_conversation = ConversationHandler(
            entry_points= [MessageHandler(filters=Filters.document, callback=self.polling_handler.save_document)],
            states={
                States.POLLING_MESSAGE: [
                    MessageHandler(filters=Filters.text, callback=self.polling_handler.get_polling_message)
                ],
                States.POLLING_NAME: [MessageHandler(
                    filters=Filters.text,
                    callback=self.polling_handler.get_polling_name,
            )],
            },
            allow_reentry=True,
            fallbacks=[]
        )
        # self.dispatcher.add_handler(register_conversation)
        self.dispatcher.add_handler(polling_conversation)
        self.dispatcher.add_handler(
            RegexHandler(pattern=Commands.report, callback=self.polling_handler.get_report)
        )
        self.dispatcher.add_handler(
            document_conversation
        )
        self.dispatcher.add_handler(
            polling_start_conversation
        )
        self.dispatcher.add_handler(
            CommandHandler(Commands.stop, callback=self.polling_handler.finish_polling)
        )
        self.dispatcher.add_handler(conversation_handler)

