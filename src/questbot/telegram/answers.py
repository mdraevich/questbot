from string import Template


class BotTemplates():
    """
    class for managing all answer templates for bot
    """

    DEFAULT_LANG_CODE = "ru"
    ANSWER_TEMPLATES = {
        "hello": {
            "ru": Template("👋 Приветствую, <b>$name</b>!\n"
                           "Я бот для организации и проведения командных квестов.\n\n"
                           "ℹ️ Выполните /help для справки по участию в квестах.")
        },
        "help": {
            "ru": Template("")
        },
        "change_nickname_success": {
            "ru": Template("✅ Никнейм изменен!")
        },
        "change_nickname_fail": {
            "ru": Template("❌ Никнейм не был изменен!\n\n"
                           "ℹ️ Убедитесь, что ваш никнейм соответствует условиям:\n"
                           "1. имеет длину <b>от 4 до 25 символов</b> (включительно);\n"
                           "2. никнейм содержит исключительно <b>буквы, цифры</b> и "
                           " <b>нижний пробел</b>.")
        },
        "help": {
            "ru": Template("🛟 <b>Справка</b>\n\n"
                           "<b>1. Пользователь</b>\n"
                           "Пользователь должен иметь никнейм, причем необязательно уникальный на сервере. "
                           "Пользователь вне квеста получает уведомления о планируемых квестах, в которых "
                           "может принять участие, нажав на соответствующую кнопку в уведомлении о квесте.\n"
                           "Зарегистрировавшись на квест, пользователь далее будет получать исключительно уведомления о "
                           "событиях в рамках выбранного квеста (начало, старт, подсказки и т.д.).\n"
                           "После окончания квеста пользователь возвращается в основной контекст, где получает "
                           "уведомления о планируемых квестах.\n"
                           "Пользователь может принудительно отказаться от участия в квесте <b>без возможности "
                           "участвовать вновь</b>.\n\n"
                           "<b>2. Команда</b>\n"\
                           "Пользователи делятся между командами поровну. Кол-во команд определяется "
                           "конфигурацией квеста и может быть произвольным.\n"
                           "Игроки в рамках одной команды имеют равные полномочия, таким образом, каждый в праве дать ответ или "
                           "запросить подсказку. Координация игроков осуществляется "
                           "посредством командного чата (указывается в конфигурации квеста).\n\n"
                           "<b>3. Квест</b>\n"\
                           "Квест состоит из произвольного кол-ва команд, для каждой из которой есть "
                           "подготовленный набор заданий.\n"
                           "Задания имеет структуру из одного вопроса, нуля или нескольких подсказок и одного ответа. "
                           "За использование подсказки или дачу неправильного ответа предусмотрен штраф команде. "
                           "Выполнение квеста ограничивается по времени.\n\n"
                           "<b>4. Команды бота</b>\n"\
                           "▫️/start — регистрация пользователя\n"
                           "▫️/help — помощь по боту\n"
                           "▫️/nickname НИКНЕЙМ — смена никнейма\n"
                           "▫️/register ИДЕНТИФИКАТОР — зарегистрироваться на квест\n"
                           "▫️/unregister — отказаться от участия в квесте\n"
                           "▫️/aboutquest — информация о текущем квесте\n"
                           "▫️/aboutteam — информация о команде\n"
                           "▫️/aboutme — информация о тебе\n"
                           "▫️/answer ОТВЕТ — дать ответ в текущем квесте\n"
                           "▫️/hint — запросить подсказку в текущем квесте\n")
        },
        "quest_scheduled": {
            "ru": Template("💬 <b>Доступен новый квест!</b>\n\n"
                           "<b>Начало</b>: $date\n"
                           "<b>Длительность</b>: $duration\n\n"
                           "<b>$quest_name</b>\n"
                           "<i>$quest_description</i>\n\n"
                           "<b>Участвующие команды:</b>\n"
                           "$teams\n\n"
                           "⚠️ <b>Для участия выполните следующую команду:</b>\n"
                           "<code>/register $qevent_id</code>"
                           ""
                           "")
        },
        "register_qevent_success": {
            "ru": Template("✅ Ты успешно зарегистрировался на квест #$qevent_id!")
        },
        "register_qevent_fail": {
            "ru": Template("❌ Ошибка!\nПроверьте корректность команды регистрации.")
        },
        "unregister_success": {
            "ru": Template("🏃‍♂️ Ты покинул квест, на который был зарегистрирован.")
        },
        "unregister_fail": {
            "ru": Template("❌ Ты не зарегистрировался на квест, чтобы покинуть его.")
        },
        "give_answer_fail": {
            "ru": Template("❌ Ты не участвуешь в квесте, чтобы прислать ответ.")
        },
        "give_answer_wrong_format": {
            "ru": Template("❌ Ответ не принят, так как не удовлетворяет условиям:\n"
                           "1. содержит от 1 до 25 символов;\n"
                           "2. содержит исключительно буквы, цифры и нижнее "
                           "подчеркивание.")
        },
        "get_hint_fail": {
            "ru": Template("❌ Ты не участвуешь в квесте, чтобы запросить подсказку.")
        },
        "quest_started_info": {
            "ru": Template("📣 <b>Квест начинается</b>!\n\n"
                           "<i>$team_description</i>\n"
                           "<a href='$team_communication'>Командный чат</a>")
        },
        "quest_new_task": {
            "ru": Template("📣 <b>Получено новое задание</b>!\n\n"
                           "<i>$task_question</i>")
        },
        "quest_no_tasks_left": {
            "ru": Template("📣 <b>Вы выполнили все задания</b>!")
        },
        "quest_wrong_answer": {
            "ru": Template("⚠️ <b>$username</b> прислал неверный ответ — <i>$answer</i>!")
        },
        "quest_correct_answer": {
            "ru": Template("✅ <b>$username</b> прислал правильный ответ — <i>$answer</i>!")
        },
        "get_hint_success": {
            "ru": Template("ℹ️ <b>$username</b> запросил для команды подсказку!\n\n"
                           "<i>$task_hint</i>")
        },
        "get_hint_empty": {
            "ru": Template("ℹ️ <b>$username</b> запросил для команды подсказку, "
                           "но подсказки уже закончились.")
        },
    }

    def get_answer_template(self, template_name, prefer_lang_code):
        """
        returns answer template for specified name and preferred lang code
        """

        if template_name not in self.ANSWER_TEMPLATES:
            raise KeyError(f"Cannot find an answer template with "
                           f"template_name={template_name}")
        if prefer_lang_code not in self.ANSWER_TEMPLATES[template_name]:
            lang_code = self.DEFAULT_LANG_CODE
        else:
            lang_code = prefer_lang_code

        return self.ANSWER_TEMPLATES[template_name][lang_code]