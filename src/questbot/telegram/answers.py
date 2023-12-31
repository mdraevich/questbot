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
                           "▫️<code>/start</code> — регистрация пользователя\n"
                           "▫️<code>/help</code> — помощь по боту\n"
                           "▫️<code>/register ИДЕНТИФИКАТОР</code> — зарегистрироваться на квест\n"
                           "▫️<code>/unregister</code> — отказаться от участия в квесте\n"
                           "▫️<code>/answer ОТВЕТ</code> — дать ответ в текущем квесте\n"
                           "▫️<code>/hint</code> — запросить подсказку в текущем квесте\n"
                           "▫️<code>/deleteme</code> — полное удаление профиля в боте\n")
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
            "ru": Template("✅ <b>Успех</b>!\n\nВы успешно зарегистрировались на квест #$qevent_id!")
        },
        "register_qevent_fail": {
            "ru": Template("❌ <b>Ошибка</b>!\n\nПроверьте корректность идентификатора квеста "
                           "для регистрации.\nВозможно, квест уже начался, поэтому регистрация более недоступна.")
        },
        "unregister_success": {
            "ru": Template("🏃‍♂️ Вы покинули квест, в котором участвовали.")
        },
        "unregister_fail": {
            "ru": Template("❌ <b>Ошибка</b>!\n\nВы не зарегистрировались на квест, чтобы покинуть его.")
        },
        "give_answer_fail": {
            "ru": Template("❌ <b>Ошибка</b>!\n\nВы не участвуете в квесте, чтобы прислать ответ.")
        },
        "give_answer_wrong_format": {
            "ru": Template("❌ <b>Ошибка</b>!\n\nОтвет не принят, так как не удовлетворяет условиям:\n"
                           "1. содержит от 1 до 25 символов;\n"
                           "2. содержит исключительно буквы, цифры и нижнее "
                           "подчеркивание.")
        },
        "get_hint_fail": {
            "ru": Template("❌ <b>Ошибка</b>!\n\nВы не участвуете в квесте, чтобы запросить подсказку.")
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
            "ru": Template("📣 <b>Вы выполнили все задания</b>!\n\n"
                           "Результаты будут опубликованы по окончанию квеста, чтобы сохранить интригу 😝")
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
        "quest_stopped": {
            "ru": Template("📣 <b>Квест завершен</b>!\n\n"
                           "Благодарим за участие!\n"
                           "Вы автоматически покидаете данный квест.")
        },
        "register_while_playing": {
            "ru": Template("❌ <b>Ошибка</b>!\n\n"
                           "Вы уже участвуете в квесте, поэтому не можете зарегистрироваться на другой.\n"
                           "Чтобы покинуть текущий квест, выполните /unregister.\n\n"
                           "⚠️ <b>ВНИМАНИЕ</b>: Вы не сможете вернуться в квест, если квест уже начался.")
        },
        "quest_results": {
            "ru": Template("💬 <b>Доступны результаты квеста</b>!\n\n"
                           "<b>$quest_name</b>\n"
                           "<i>$quest_description</i>\n\n"
                           "<b>Победитель</b>: $winner_name 🏆\n"
                           "<b>Список участников команды</b>:\n"
                           "$winner_players"
                           "")
        },
        "quest_results_in_detail": {
            "ru": Template("💬 <b>$team_name</b>, публикуем ваш результат!\n\n"
                           "<b>Итоговый результат</b>: $total_points 💎\n"
                           "<b>Подробная статистика</b>:\n"
                           "<code>$points_per_task</code>\n\n"
                           "ℹ️ <i>Каждый ряд отражает номер задачи, бонус за выполнение, за отсутствие штрафов и за время соответственно</i>"
                           "")
        },
        "delete_profile": {
            "ru": Template("☠️ Вы покидаете данный сервер, но вы можете вернуться, выполнив /start.\n\n"
                           "")
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