import glob


class I18N:
    def __init__(self, language, load_from_file=True):
        if load_from_file:
            if language in self.get_available_languages():
                self.load_data_from_file(language)
            else:
                raise NotImplementedError("Unsupported language. Add missing language file.")
        else:
            if language == "en":
                self.load_data_in_english()
            elif language == "tr":
                self.load_data_in_turkish()
            else:
                raise NotImplementedError("Unsupported language.")

    def load_data_in_english(self):
        self.title_filebook = "Filebook"
        self.file_name = "File Name"
        self.file_type = "File Type"
        self.file_link = "File Link"
        self.select_file="Select File"
        self.save_file = "Save"
        self.all_types="All types"
        self.text_file="Text file"
        self.pdf_file="Pdf file"
        self.file_name_empty="File name can not be empty"
        self.file_type_empty="File type can not be empty"
        self.file_link_empty="File link can not be empty"
        self.message_done="Done"
        self.message_file_saved="File saved"
        self.message_file_cannot_saved="Failed to save new file"
        self.message_file_cannot_saved_update="Failed to update new changes"
        self.update_file="Update"
        self.file_id="File ID"
        self.menubar="Add"
        self.file_menu="File"
        self.confirm_delete="Are you sure you want to delete the selected row(s)?"
        self.message_delete="Selected row(s) deleted"
        self.title_profile="Profile"
        self.create_profile_database="Create Profile Database"
        self.clear_profile_database="Clear Profile Database"
        self.database_exist="Database already exist"
        self.database_created="Database created"
        self.database_failed="Failed to create database"
        self.database_cleared="Database cleared"
        self.cleared_failed="Failed to clear database"
        self.exit_title="Exit"
        self.sure_exit="Are you sure you want to exit?"
        self.title = "Add New Habit"
        self.name = "Habit Name"
        self.type = "Habit Type"
        self.streak = "Streak"
        self.done = "Done"
        self.add_btn="Add"
        self.new_btn="New Habit +"
        self.edit_btn="Edit Habit"
        self.delete_btn="Delete Habit"
        self.id="ID"
        self.title1="Habit Tracker"
        self.title2="Edit"
        self.update_btn="Edit"
        self.title3="Calendar"
        self.lbl_today="Today: "
        self.add_task_btn="Add Task"
        self.tasks_btn="Tasks List"
        self.lbl_selected="Selected Day: "
        self.lbl_task="Task Name: "
        self.lbl_time="Date: "
        self.habitTrackerLabel="Habit Tracker"
        self.calendarLabel="Calendar"
        self.ToDoList="To Do List"
        self.warning="Warning"
        self.habit_message="Habit name cannot be empty."
        self.added_msg="Added"
        self.habit_saved="Habit saved."
        self.failed_habit_added="Failed to save new habit.\n"
        self.study="Study"
        self.work="Work"
        self.entertainment="Entertainment"
        self.other="-other-"
        self.error="Error"
        self.valuenot="Value is not acceptable."
        self.done="Done"
        self.task_saved="Task saved."
        self.failed_task_added="Failed to save new task.\n"
        self.task_msg="Task cannot be empty."
        self.not_added="The task not added"
        self.selecting_date="Please select a date"
        self.success="Success"
        self.updated_success="Habit updated successfully."
        self.failed_update="Failed to update changes."
        self.confirm_delete="Confirm Delete"
        self.sure="Are you sure you want to delete?"
        self.should_select="One habit should be selected"
        self.monthly_progress="Monthly Progress"
        self.done_month="Done for a month:"


    def load_data_in_turkish(self):
        self.title_filebook = "Dosyalık"
        self.file_name = "Dosya Adı"
        self.file_type = "Dosya Konusu"
        self.file_link = "Dosya Türü"
        self.select_file="Dosya seç"
        self.save_file = "Kaydet"
        self.all_types="Bütün dosya türleri"
        self.text_file="Metin dosyaları"
        self.pdf_file="Pdf dosyaları"
        self.file_name_empty="Dosya adı boş bırakılamaz"
        self.file_type_empty="Dosya türü boş bırakılamaz"
        self.file_link_empty="Dosya linki boş bırakılamaz"
        self.message_done="Tamamlandı"
        self.message_file_saved="Dosya kaydedildi"
        self.message_file_cannot_saved="Dosya bilgileri kaydedilemedi"
        self.message_file_cannot_saved_update="Dosya bilgileri güncellenemedi"
        self.update_file="Güncelle"
        self.file_id="Dosya ID"
        self.menubar="Ekle"
        self.file_menu="Dosya"
        self.confirm_delete="Seçilen satır ya da satırları silmek istediğinden emin misin?"
        self.message_delete="Seçilen satırlar silindi"
        self.title_profile="Profil"
        self.create_profile_database="Profil Veri Tabanını Oluştur"
        self.clear_profile_database="Profil Veri Tabanını Sil"
        self.database_exist="Veri Tabanı zaten mevcut"
        self.database_created="Veri tabanı oluşturuldu"
        self.database_failed="Veri tabanı oluşturulamadı"
        self.database_cleared="Veri tabanı silindi"
        self.cleared_failed="Veri tabanı silinemedi"
        self.exit_title="Çıkış"
        self.sure_exit="Çıkmak istediğinize emin misiniz?"
        self.title = "Yeni Alışkanlık Ekle"
        self.name = "Alışkanlık adı"
        self.type = "Alışkanlık tipi"
        self.streak = "Ateş"
        self.done = "Yapıldı"
        self.add_btn="Ekle"
        self.new_btn="Yeni Alışkanlık +"
        self.edit_btn="Alışkanlığı Düzenle"
        self.delete_btn="Alışkanlığı Sil"
        self.id="NO"
        self.title1="Alışkanlık Takibi"
        self.title2="Güncelle"
        self.update_btn="Güncelle"
        self.title3="Takvim"
        self.lbl_today="Bugün: "
        self.add_task_btn="Görev Ekle"
        self.tasks_btn="Görev Listesi"
        self.lbl_selected="Seçilen Gün: "
        self.lbl_task="Görevin Adı: "
        self.lbl_time="Tarih: "
        self.habitTrackerLabel="Alışkanlık Takibi"
        self.calendarLabel="Takvim"
        self.ToDoList="Yapılacaklar Listesi"
        self.warning="Uyarı"
        self.habit_message="Alışkanlık adı boş olamaz."
        self.added_msg="Eklendi"
        self.habit_saved="Alışkanlık kaydedildi."
        self.failed_habit_added="Yeni alışkanlık kaydedilirken hata oluştu.\n"
        self.study="Ders"
        self.work="İş"
        self.entertainment="Eğlence"
        self.other="-diğer-"
        self.error="Hata"
        self.valuenot="Girilen değer uygun değildir."
        self.done="Tamamlandı"
        self.task_saved="Görev kaydedildi."
        self.failed_task_added="Yeni görev kaydedilirken hata oluştu.\n"
        self.task_msg="Görev boş bırakılamaz."
        self.not_added="Görev eklenemedi"
        self.selecting_date="Lütfen , bir tarih seçin"
        self.success="Başarılı"
        self.updated_success="Alışkanlık güncellemesi başarıyla sonuçlanmıştır.."
        self.failed_update="Değişiklikleri kaydederken hata oluştu."
        self.confirm_delete="Silmeyi Onayla"
        self.sure="Silmek istediğinize emin misiniz?"
        self.should_select="Bir alışkanlık seçilmelidir."
        self.monthly_progress="Aylık Süreç"
        self.done_month="Bir ay içinde yapılan:"


    def load_data_from_file(self, lang):
        lang_data = {}
        lang_file = f"data_{lang}.lng"
        with open(file=lang_file, encoding="utf-8") as f:
            for line in f:
                if not line.strip() or '=' not in line:
                  continue
                (key, val) = line.strip().split("=")
                lang_data[key] = val

        self.title_filebook=lang_data["title_filebook"]
        self.file_name=lang_data["file_name"]
        self.file_type=lang_data["file_type"]
        self.file_link=lang_data["file_link"]
        self.select_file=lang_data["select_file"]
        self.save_file=lang_data["save_file"]
        self.all_types=lang_data["all_types"]
        self.text_file=lang_data["text_file"]
        self.pdf_file=lang_data["pdf_file"]
        self.file_name_empty=lang_data["file_name_empty"]
        self.file_type_empty=lang_data["file_type_empty"]
        self.file_link_empty=lang_data["file_link_empty"]
        self.message_done=lang_data["message_done"]
        self.message_file_saved=lang_data["message_file_saved"]
        self.message_file_cannot_saved=lang_data["message_file_cannot_saved"]
        self.message_file_cannot_saved_update=lang_data["message_file_cannot_saved_update"]
        self.update_file=lang_data["update_file"]
        self.file_id=lang_data["file_id"]
        self.menubar=lang_data["menubar"]
        self.file_menu=lang_data["file_menu"]
        self.confirm_delete=lang_data["confirm_delete"]
        self.message_delete=lang_data["message_delete"]
        self.title_profile=lang_data["title_profile"]
        self.create_profile_database=lang_data["create_profile_database"]
        self.clear_profile_database=lang_data["clear_profile_database"]
        self.database_exist=lang_data["database_exist"]
        self.database_created=lang_data["database_created"]
        self.database_failed=lang_data["database_failed"]
        self.database_cleared=lang_data["database_cleared"]
        self.cleared_failed=lang_data["cleared_failed"]
        self.exit_title=lang_data["exit_title"]
        self.sure_exit=lang_data["sure_exit"]
        self.title = lang_data["title"]
        self.name = lang_data["name"]
        self.type = lang_data["type"]
        self.streak = lang_data["streak"]
        self.done = lang_data["done"]
        self.add_btn = lang_data["add_btn"]
        self.new_btn = lang_data["new_btn"]
        self.edit_btn = lang_data["edit_btn"]
        self.delete_btn = lang_data["delete_btn"]
        self.id=lang_data["id"]
        self.title1=lang_data["title1"]
        self.title2=lang_data["title2"]
        self.update_btn = lang_data["update_btn"]
        self.title3=lang_data["title3"]
        self.lbl_today=lang_data["lbl_today"]
        self.add_task_btn=lang_data["add_task_btn"]
        self.tasks_btn=lang_data["tasks_btn"]
        self.lbl_selected=lang_data["lbl_selected"]
        self.lbl_task=lang_data["lbl_task"]
        self.lbl_time=lang_data["lbl_time"]
        self.habitTrackerLabel=lang_data["habitTrackerLabel"]
        self.calendarLabel=lang_data["calendarLabel"]
        self.ToDoList=lang_data["ToDoList"]
        self.warning=lang_data["warning"]
        self.habit_message=lang_data["habit_message"]
        self.added_msg=lang_data["added_msg"]
        self.habit_saved=lang_data["habit_saved"]
        self.failed_habit_added=lang_data["failed_habit_added"]
        self.study=lang_data["study"]
        self.work=lang_data["work"]
        self.entertainment=lang_data["entertainment"]
        self.other=lang_data["other"]
        self.error=lang_data["error"]
        self.valuenot=lang_data["valuenot"]
        self.done=lang_data["done"]
        self.task_saved=lang_data["task_saved"]
        self.failed_task_added=lang_data["failed_task_added"]
        self.task_msg=lang_data["task_msg"]
        self.not_added=lang_data["not_added"]
        self.selecting_date=lang_data["selecting_date"]
        self.success=lang_data["success"]
        self.updated_success=lang_data["updated_success"]
        self.failed_update=lang_data["failed_update"]
        self.confirm_delete_title =lang_data["confirm_delete_title"]
        self.sure=lang_data["sure"]
        self.should_select=lang_data["should_select"]
        self.monthly_progress=lang_data["monthly_progress"]
        self.done_month=lang_data["done_month"]

        # todolist için 
        self.status = lang_data["status"]
        self.task=lang_data["task"]
        self.deadline=lang_data["deadline"]
        self.dodate=lang_data["dodate"]
        self.priority=lang_data["priority"]
        self.tags=lang_data["tags"]
        self.tag=lang_data["tags"]
        self.in_progress=lang_data["in_progress"]
        self.not_started=lang_data["not_started"]
        self.low=lang_data["low"]
        self.medium=lang_data["medium"]
        self.high=lang_data["high"]
        self.clear=lang_data["clear"]
        self.select=lang_data["select"]
        self.msg_enter_task=lang_data["msg_enter_task"]
        self.msg_update_success = lang_data["msg_update_success"]
        self.update_task = lang_data["update_task"]
        self.add_reminder=lang_data["add_reminder"]
        self.rem_list=lang_data["rem_list"]
        self.reminders=lang_data["reminders"]
        self.rem_name=lang_data["rem_name"]
        self.rem_saved=lang_data["rem_saved"]
        self.failed_rem_added=lang_data["failed_rem_added"]
        self.empty_rem_msg=lang_data["empty_rem_msg"]
        self.invalid_date_msg=lang_data["invalid_date_msg"]




    @staticmethod
    def get_available_languages():
        language_files = glob.glob("*.lng")
        language_codes = []
        for f in language_files:
            language_code = f.replace("data_", "").replace(".lng", "")
            language_codes.append(language_code)
        return language_codes
