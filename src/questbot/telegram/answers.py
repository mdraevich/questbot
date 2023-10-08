from string import Template

default_lang_code = "ru"
answer_templates = {
    "hello": {
        "ru": Template("👋 Приветствую, <b>$name</b>!\n"
                       "Я бот для организации и проведения командных квестов.\n\n"
                       "ℹ️ Твой никнейм был сгенерирован автоматически мною, но ты можешь "
                       "поменять его, выполнив следующую команду: \n"
                       "<code>/nickname НОВЫЙ-НИКНЕЙМ</code>")
    },
    "help": {
        "ru": Template("")
    },
    "nickname": {
        "ru": Template("✅ Никнейм изменен!")
    }
}