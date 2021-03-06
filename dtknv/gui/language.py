#! /usr/bin/python3

"""

Strings for the GUI.

"""

__version__ = '0.5'

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
'menu_settings_excfiles':'Изузеци у употреби',
'menu_settings_tocyr':'Из латинице у ћирилицу',
'menu_settings_tolat':'Из ћирилице у латиницу',
'menu_settings_language':'Језик сучеља',
'menu_settings_lngcyr':'Српски (ћирлица)',
'menu_settings_lnglat':'Srpski (latinica)',
'menu_settings_lngeng':'English',
'menu_help':'Помоћ',
'menu_help_help':'Упутство',
'menu_help_update':'Нова верзија...',
'menu_help_about':'О програму',
'window_exceptions':'Изузеци',
'window_about':'О програму',
'button_ok':'Потврди',
'button_convert':'Конвертуј <F5>',
'button_cancel':'Откажи',
'button_close':'Затвори',
'button_load':'Учитај... ↓',
'button_saveexc':'Сачувај ниске <ctrl + s>',
'button_addcells':'Додај ред ћелија <ctrl + d>',
'button_fileexc':'Датотеку %s',
'button_newexcfile':'Нова датотека изузетака... <ctrl + n>',
'button_removecells':'Избриши одабрани ред <ctrl + i>',
'button_csv_import':'Увези CSV датотеку...',
'button_csv_export':'Извези CSV датотеку...',
'button_erase':'Избриши',
'button_tolat':'У латиницу',
'button_default':'Врати подешавања',
'button_tocyr':'У ћирилицу',
'button_exc_commands':'Команде... ↓',
'button_standardsr':'Стандардни ћирилични изузеци',
'window_options':'Подешавања',
'options_verbose':'Приказуј детаље у конзоли',
'options_failsafe':'Обустави након прве грешке',
'options_noram':'Користи хард диск за распакивање (није препоручљиво)',
'options_report':'Прави извјештаје о раду',
'options_reportname':'Име датотеке за извјештај:',
'options_encoding':'Кодна страна:',
'options_warningmb':'Број мегабајта прије упозорења:',
'options_warningn':'Број датотека прије упозорења:',
'options_extensions':'Препознате екстензије (Ћ > Л): ',
'options_extensions_tocyr':'Препознате екстензије (Л > Ћ): ',
'options_reportpath':'Фасцикла за извјештаје\n(двоклик за одабир): ',
'status_mode_filesdir':'Датотеке и фасцикле.',
'status_mode_plaintext':'Обичан текст.',
'msg_settingschanged':'Подешавања су промијењена. Сачувати?',
'msg_sameinout':'Да би улазна и излазна путања биле исте, морате\n' + \
                'укључити опцију "Сачувај у истој фасцикли"\n\n' + \
                'Укључити ову опцију?',
'msg_savechanges':'Сачувати промјене?',
'msg_extension_not_supported':'Та врста датотеке није дозвољена у ћир. конверзији.',
'msg_nolocalhelp':'Немате инсталирано упутство на рачунару.\n' + \
                   'Отворити верзију на званичном сајту?',
'msg_nohelpinenglish':'Програм нема упутство на енглеском.',
'msg_error_opening_report':'Грешка приликом отварања извјештаја\n (%s).',
'msg_report_not_created':'Извјештај није креиран (укључите га у подешавањима).',
'label_save':'Сачувати',
'label_type':'Врста: ',
'label_updateerror':'Прогам није могао провјерити да ли је' + \
    ' објављена нова верзија. ',
'label_updatenonew':'Користите најновије издање програма, верзију %s.',
'label_updatechecking':'Тренутак, провјера у току...',
'label_updatenew':'Доступна је нова  верзија, %s (%s).\n\nНовости:\n%s',
'label_updatdirect':'Директно преузимање >>>',
'label_updatepage':'Страница за преузимање >>>',
'label_datechanged':'Посљедња измјена: ',
'label_file':'Датотека: ',
'label_finishedcheck':' Провјерите датотеке и извјештај.',
'label_no_report':' Извјештај није креиран.',
'label_conversion':'Конверзија.',
'label_finishedwitherrors':'Завршено, уз грешке. ',
'label_finished':'Завршено.',
'label_dir':'Фасцикла: ',
'label_size':'Укупно: %s МБ',
'label_dirout':'Сачувати у: ',
'label_number':'Брoj датотека: %s',
'label_ready':' Све је спремно за конверзију.',
'label_pleasewait':' Тренутак... Израчунавање у току.',
'label_nosupportedfiles':' У одабраној фасцикли нема подржаних датотека.',
'label_invalidchar':'Назив датотеке садржи недозвољени знак.',
'label_enterfilenameexc':'Унесите назив датотеке за нове изузетке:',
'label_fieldsblank':'Ћелије у првој колони не смију бити празне.',
'label_fieldsrepeat':'Вриједности у првој колони не смију се понављати.',
'label_ok':' ОК.',
'label_error':'Грешка у учитавању датотеке.\nОдаберите другу или направите нову.',
'label_error_loadingexc':'Грешка',
'label_error_generic':'Грешка',
'label_filealreadyexists': 'Датотека %s већ постоји.',
'label_convtolat':'Конверзија у латиницу.',
'label_convtocyr':'Конверзија у ћирилицу.',
'label_about_desc':'Дткнв, латинично-ћирилични конвертор (верзија %s).',
'label_about_author':'Ромео Млинар',
'label_about_year':'2010-2012',
'label_about_license':'Овај програм је бесплатан и слободан, објављен под ' + \
    'условима GPL3 лиценце.',
'label_about_mail':'Све предлоге и грешке пошаљите на ' + \
    'mlinar--a--languagebits.com. Хвала! :)',
'label_about_name':'Дткнв',
'title_open_file':'Одабир датотеке',
'title_open_dirin':'Одабир улазне фасцикле',
'title_open_dirout':'Одабир излазне фасцикле',
'title_open_dir':'Одабир фасцикле',
'ext_html':'хипертекст ',
'ext_htm':'хипертекст ',
'ext_odt':'Опенофис / Либреофис документ',
'ext_docx':'Ворд 2007+ документ',
'ext_txt':'обичан текст ',
'ext_*':'све датотеке ',
'ext_?generic':'датотеке типа '
}

english = {

# Language strings for Serbian Cyrillic (converted automatically
# to Serbian Latin, if selected).

'menu_main':'File',
'menu_file_loadf':'Load file... <ctrl + o>',
'menu_file_loadd':'Load directory... <ctrl + f>',
'menu_file_outpath':'Save in...  <ctrl + u>',
'menu_file_exit':'Exit',
'menu_settings':'Options',
'menu_settings_samedir':'Save in same folder',
'menu_settings_names':'Convert file names',
'menu_settings_recur':'Recursive conversion',
'menu_settings_adv':'Advanced settings... <F3>',
'menu_settings_showfilesdir':'File conversion <F7>',
'menu_settings_showplaintext':'Plain text conversion <F8>',
'menu_settings_exceptions':'Exceptions... <F2>',
'menu_settings_excfiles':'Exceptions in use',
'menu_settings_tocyr':'From Latin to Cyrillic',
'menu_settings_tolat':'From Cyrillic to Latin',
'menu_settings_language':'Interface language',
'menu_settings_lngcyr':'Serbian (Cyrillic)',
'menu_settings_lnglat':'Serbian (Latin)',
'menu_settings_lngeng':'English',
'menu_help':'Help',
'menu_help_help':'Howto',
'menu_help_update':'New versions...',
'menu_help_about':'About the program',
'window_exceptions':'Exceptions',
'window_about':'About the program',
'button_ok':'OK',
'button_convert':'Convert <F5>',
'button_cancel':'Cancel',
'button_close':'Close',
'button_load':'Load... ↓',
'button_saveexc':'Save strings <ctrl + s>',
'button_addcells':'Add cells row <ctrl + d>',
'button_fileexc':'File %s',
'button_newexcfile':'New exception file... <ctrl + n>',
'button_removecells':'Erase selected row <ctrl + i>',
'button_csv_import':'Import CSV file...',
'button_csv_export':'Esport CSV file...',
'button_erase':'Erase',
'button_tolat':'To Latin',
'button_default':'Default',
'button_tocyr':'To Cyrillic',
'button_exc_commands':'Actions... ↓',
'button_standardsr':'Default Cyrillic exceptions',
'window_options':'Options',
'options_verbose':'Show details in console',
'options_failsafe':'Abort on error',
'options_noram':'Use hard disk to unpack (not recommended)',
'options_report':'Create reports',
'options_reportname':'Report file name :',
'options_encoding':'Encoding:',
'options_warningmb':'The number of MBs before warning:',
'options_warningn':'The number of files before warning:',
'options_extensions':'Recognised extensions (C > L): ',
'options_extensions_tocyr':'Recognised extensions (L > C): ',
'options_reportpath':'Save reports to folder \n(double click to select): ',
'status_mode_filesdir':'Files and folders.',
'status_mode_plaintext':'Plain text.',
'msg_settingschanged':'The settings are changed. Save?',
'msg_sameinout':'To have the same in and out paths you must\n' + \
                'turn on "Save in the same folder"\n\n' + \
                'Turn the option on?',
'msg_savechanges':'Save changes?',
'msg_extension_not_supported':'That extension must be allowed ' + \
    'for this conversion.',
'msg_error_opening_report':'Error while opening the report\n (%s).',
'msg_report_not_created':'Report is off (turn it on in settings).',
'label_save':'Save',
'label_type':'Type: ',
'label_updateerror':'The program could not check if there is' + \
    ' a new version available. ',
'label_updatenonew':'You are using the newest program edition, version %s.',
'label_updatechecking':'Plese wait while checking...',
'label_updatenew':'The new version is available, %s (%s).\n\nWhat is new:\n%s',
'label_updatdirect':'Direct download link >>>',
'label_updatepage':'The download page >>>',
'label_datechanged':'Last change: ',
'label_file':'File: ',
'label_finishedcheck':' Check your files and the report.',
'label_no_report':' A report is not created.',
'label_conversion':'Conversion.',
'label_finishedwitherrors':'Completed, with some errors. ',
'label_finished':'Completed.',
'label_dir':'Folder: ',
'label_size':'Combined: %s MB',
'label_dirout':'Save in: ',
'label_number':'Number of files: %s',
'label_ready':' Ready for the conversion.',
'label_pleasewait':' Please wait while calculating...',
'label_nosupportedfiles':' No supported files in the slected folder.',
'label_invalidchar':'An invalid character is present in the file name.',
'label_enterfilenameexc':'Enter the file name for new exception file:',
'label_fieldsblank':'The cells in the first column must not be empty.',
'label_fieldsrepeat':'The values in the first column must be unique.',
'label_ok':' ОК.',
'label_error':'Error',
'label_filealreadyexists': 'File %s already exists.',
'label_error_generic':'Error',
'label_convtolat':'Conversion to Latin.',
'label_convtocyr':'Conversion to Cyrillic.',
'label_about_desc':'Dtknv, the Serbian alphabet transliterator (version %s).',
'label_about_author':'Romeo Mlinar',
'label_about_year':'2010-2011',
'label_about_license':'This program is free, published under the terms of ' + \
    'GPL3 license.',
'label_about_mail':'Please send all your suggestions or bug reports to ' + \
    'mlinar--a--languagebits.com. Thank you! :)',
'label_about_name':'Dtknv',
'title_open_file':'File selection',
'title_open_dirin':'Input folder selection',
'title_open_dirout':'Output folder selection',
'title_open_dir':'Folder selection',
'ext_html':'hypertext ',
'ext_htm':'hypertext ',
'ext_odt':'OpenOffice / LibreOffice document',
'ext_docx':'Word 2007+ document',
'ext_txt':'plain text ',
'ext_*':'all files ',
'ext_?generic':'a file of the type ',

#This one is for English only
'msg_nohelpinenglish':'Help files are available in Serbian only.'

}


multilanguage = {

# Multilanguage strings that can be called independently from the main
# language strings.

'lngcyr_msg_restart':'За промјену језика поново покрените\n програм.', 
'lnglat_msg_restart':'Za promjenu jezika ponovo pokrenite\nprogram.',
'lngeng_msg_restart':'To change the language restart the program.'          
         
}
