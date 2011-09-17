#! /usr/bin/python3

"""

Strings for the GUI.

"""

serbian_cyrillic = {

# Language strings for Serbian Cyrillic (converted automatically
# to Serbian Latin, if selected).

'menu_main':'Датотека',
'menu_file_loadf':'Учитај датотеку... <ctrl + o>',
'menu_file_loadd':'Учитај фасциклу... <ctrl + f>',
'menu_file_outpath':'Сачувај у...  <ctrl + u>',
'menu_file_exit':'Затвори',
'menu_settings':'Опције',
'menu_settings_samedir':'Сачувај у истој фасцикли',
'menu_settings_names':'Конвертуј називе',
'menu_settings_recur':'Рекурзивна конверзија',
'menu_settings_adv':'Напредна подешавања... <F3>',
'menu_settings_showfilesdir':'Конверзија датотека <F7>',
'menu_settings_showplaintext':'Конверзија обичног текста <F8>',
'menu_settings_exceptions':'Изузеци... <F2>',
'menu_settings_language':'Језик сучеља',
'menu_settings_lngcyr':'Српски (ћирлица)',
'menu_settings_lnglat':'Srpski (latinica)',
'menu_settings_lngeng':'English',
'menu_help':'Помоћ',
'menu_help_help':'Упутство',
'menu_help_about':'О програму',
'window_exceptions':'Изузеци',
'button_ok':'Потврди',
'button_convert':'Конвертуј <F5>',
'button_cancel':'Откажи',
'button_close':'Затвори',
'button_load':'Учитај ↓',
'button_save':'Сачувај',
'button_add':'Додај',
'button_remove':'Уклони',
'button_erase':'Избриши',
'button_tolat':'У латиницу',
'button_tocyr':'У ћилирцу',
'button_standardsr':'Стандардни ћирилични изузеци',
'window_options':'Подешавања',
'options_update':'Провјери да ли је објављена нова верзија',
'options_verbose':'Приказуј детаље у конзоли',
'options_failsafe':'Обустави након прве грешке',
'options_noram':'Користи хард диск за распакивање\n(успорава рад програма!)',
'options_report':'Прави извјештаје о раду',
'options_reportname':'Име датотеке за извјештај:',
'options_encoding':'Кодна страна:',
'options_warningmb':'Број мегабајта прије упозорења:',
'options_warningn':'Број датотека прије упозорења:',
'options_extensions':'Препознате екстензије: ',
'options_reportpath':'Фасцикла за извјештаје\n(двоклик за одабир): ',
'status_mode_filesdir':'Датотеке и фасикле.',
'status_mode_plaintext':'Обичан текст.',
'msg_settingschanged':'Подешавања су промијењена. Сачувати?',
'msg_sameinout':'Да би улазна и излазна путања биле исте, морате\n' + \
                'укључити опцију "Сачувај у истој фасцикли"\n\n' + \
                'Укључити ову опцију?',
'label_type':'Врста: ',
'label_datechanged':'Посљеднја измјена: ',
'label_file':'Датотека: ',
'label_dir':'Фасцикла: ',
'label_size':'Укупно: %s МБ',
'label_dirout':'Сачувати у: ',
'label_number':'Брoj датотека: %s',
'label_ready':' Све је спремно за конверзију.',
'label_pleasewait':' Тренутак... Израчунавање у току.',
'label_nosupportedfiles':' У одабраној фасцикли нема подржаних датотека.',
'label_ok':' ОК.',
'ext_html':'хипертекст ',
'ext_htm':'хипертекст ',
'ext_odt':'Опенофис / Либреофис документ',
'ext_docx':'Ворд 2007+  документ',
'ext_txt':'обичан текст '
}


multilanguage = {

# Multilanguage strings that can be called independently from the main
# language strings.

'lngcyr_msg_restart':'За промјену језика поново покрените\n програм.', 
'lnglat_msg_restart':'Za promjenu jezika ponovo pokrenite\nprogram.',
'lngeng_msg_restart':'To change the language restart the program.'          
         
}
