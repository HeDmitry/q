import flet as ft
import random

# ================= ДАННЫЕ ВАРИАНТОВ =================
VARIANTS = {
    1: {"key": "!#%&*+=/?:;~", "alpha": {"А":"У", "Б":"П", "В":"Щ", "Г":"Д", "Д":"С", "Е":"Ю", "Ё":"Ж", "Ж":"Я", "З":"Г", "И":"К", "Й":"Ь", "К":"Ф", "Л":"Х", "М":"Ъ", "Н":"Р", "О":"И", "П":"Ч", "Р":"Ш", "С":"Б", "Т":"О", "У":"З", "Ф":"В", "Х":"М", "Ц":"Ё", "Ч":"Т", "Ш":"А", "Щ":"Л", "Ъ":"Э", "Ы":"Н", "Ь":"Е", "Э":"Й", "Ю":"Ц", "Я":"Ы"}, "punct": {".":"0", ",":"1", "!":"2", "?":"3", ":":"4", "-":"5", "(":"6", ")":"7"}},
    2: {"key": "^$@_}{|][><\\", "alpha": {"А":"К", "Б":"Э", "В":"Ю", "Г":"Д", "Д":"Н", "Е":"Ь", "Ё":"Ц", "Ж":"Г", "З":"Ш", "И":"Л", "Й":"Ф", "К":"О", "Л":"Ы", "М":"П", "Н":"Я", "О":"И", "П":"С", "Р":"М", "С":"Т", "Т":"А", "У":"В", "Ф":"Р", "Х":"Щ", "Ц":"Ё", "Ч":"З", "Ш":"Ъ", "Щ":"Б", "Ъ":"У", "Ы":"Ж", "Ь":"Х", "Э":"Ч", "Ю":"Й", "Я":"Е"}, "punct": {".":"8", ",":"7", "!":"6", "?":"5", ":":"4", "-":"3", "(":"2", ")":"1"}},
    3: {"key": "*&!%?/-+()$~", "alpha": {"А":"Х", "Б":"М", "В":"Я", "Г":"Б", "Д":"Ю", "Е":"И", "Ё":"Т", "Ж":"Ь", "З":"Г", "И":"Щ", "Й":"С", "К":"П", "Л":"Д", "М":"А", "Н":"Ц", "О":"Р", "П":"З", "Р":"Ы", "С":"Ф", "Т":"О", "У":"Н", "Ф":"Л", "Х":"Э", "Ц":"Ч", "Ч":"В", "Ш":"Е", "Щ":"Ж", "Ъ":"К", "Ы":"Ъ", "Ь":"Ш", "Э":"Й", "Ю":"Ё", "Я":"У"}, "punct": {".":"1", ",":"2", "!":"3", "?":"4", ":":"5", "-":"6", "(":"7", ")":"8"}},
    4: {"key": "><}{][:;=+#/", "alpha": {"А":"Р", "Б":"Л", "В":"О", "Г":"Ж", "Д":"Э", "Е":"Ф", "Ё":"С", "Ж":"Я", "З":"М", "И":"К", "Й":"Ъ", "К":"А", "Л":"З", "М":"Щ", "Н":"Г", "О":"П", "П":"Ц", "Р":"Ь", "С":"И", "Т":"У", "У":"Ч", "Ф":"Ы", "Х":"Б", "Ц":"Н", "Ч":"Д", "Ш":"Ё", "Щ":"Ш", "Ъ":"В", "Ы":"Т", "Ь":"Ю", "Э":"Е", "Ю":"Й", "Я":"Х"}, "punct": {".":"9", ",":"0", "!":"1", "?":"2", ":":"3", "-":"4", "(":"5", ")":"6"}},
    5: {"key": "@#^&*()_+-=|", "alpha": {"А":"Й", "Б":"Ю", "В":"Д", "Г":"Щ", "Д":"С", "Е":"К", "Ё":"Н", "Ж":"Т", "З":"Я", "И":"З", "Й":"Ь", "К":"В", "Л":"Ч", "М":"Л", "Н":"А", "О":"Ё", "П":"Х", "Р":"П", "С":"Э", "Т":"М", "У":"Ж", "Ф":"Ш", "Х":"Б", "Ц":"У", "Ч":"Ы", "Ш":"Р", "Щ":"И", "Ъ":"Г", "Ы":"Е", "Ь":"О", "Э":"Ц", "Ю":"Ф", "Я":"Ъ"}, "punct": {".":"5", ",":"4", "!":"3", "?":"2", ":":"1", "-":"0", "(":"9", ")":"8"}}
}

for v_id, data in VARIANTS.items():
    data["rev_alpha"] = {v: k for k, v in data["alpha"].items()}
    data["rev_punct"] = {v + '\u200B': k for k, v in data["punct"].items()}


def main(page: ft.Page):
    page.title = "Шифратор"
    page.theme_mode = ft.ThemeMode.DARK # Темная тема из коробки
    page.vertical_alignment = ft.MainAxisAlignment.START
    
    # Обновленное управление окном
    page.window.width = 450
    page.window.height = 700

    def show_error(message):
        # Окраска ошибок с помощью ft.Colors
        page.snack_bar = ft.SnackBar(ft.Text(message), bgcolor=ft.Colors.ERROR)
        page.snack_bar.open = True
        page.update()

    def encrypt(e):
        text = input_field.value.strip()
        if not text:
            return

        text = text.replace('\u200B', '')
        variant_id = random.choice(list(VARIANTS.keys()))
        variant = VARIANTS[variant_id]
        key = variant["key"]
        
        mapped_text = ""
        for char in text:
            upper_char = char.upper()
            if upper_char in variant["alpha"]:
                mapped_char = variant["alpha"][upper_char]
                mapped_text += mapped_char.lower() if char.islower() else mapped_char
            elif char in variant["punct"]:
                mapped_text += variant["punct"][char] + '\u200B'
            else:
                mapped_text += char

        encrypted_result = ""
        for i in range(max(len(mapped_text), 12)):
            if i < len(mapped_text):
                encrypted_result += mapped_text[i]
            if i < 12:
                encrypted_result += key[i]

        output_field.value = encrypted_result
        page.update()

    def decrypt(e):
        ciphertext = input_field.value.strip()
        if not ciphertext:
            return

        if len(ciphertext) < 12:
            show_error("Ошибка: Текст должен содержать минимум 12 символов ключа.")
            return

        text_len = len(ciphertext) - 12
        clean_text = ""
        extracted_key = ""
        
        idx = 0
        for i in range(max(text_len, 12)):
            if i < text_len:
                clean_text += ciphertext[idx]
                idx += 1
            if i < 12:
                extracted_key += ciphertext[idx]
                idx += 1

        active_variant = None
        for v_id, data in VARIANTS.items():
            if data["key"] == extracted_key:
                active_variant = data
                break
        
        if not active_variant:
            show_error("Ошибка: Не удалось распознать ключ. Текст поврежден.")
            return

        decrypted_result = ""
        i = 0
        while i < len(clean_text):
            char = clean_text[i]
            if i + 1 < len(clean_text) and clean_text[i+1] == '\u200B':
                token = char + '\u200B'
                if token in active_variant["rev_punct"]:
                    decrypted_result += active_variant["rev_punct"][token]
                else:
                    decrypted_result += char
                i += 2
            else:
                upper_char = char.upper()
                if upper_char in active_variant["rev_alpha"]:
                    dec_char = active_variant["rev_alpha"][upper_char]
                    decrypted_result += dec_char.lower() if char.islower() else dec_char
                else:
                    decrypted_result += char
                i += 1

        output_field.value = decrypted_result
        page.update()

    # Интерфейс
    input_field = ft.TextField(label="Ввод текста:", multiline=True, min_lines=5, max_lines=7, text_size=16)
    output_field = ft.TextField(label="Вывод текста:", multiline=True, min_lines=5, max_lines=7, text_size=16)
    
    # Иконки и цвета прописаны через ft.Icons и ft.Colors
    btn_encrypt = ft.ElevatedButton("Зашифровать", on_click=encrypt, icon=ft.Icons.LOCK, color=ft.Colors.WHITE, bgcolor=ft.Colors.BLUE_700)
    btn_decrypt = ft.ElevatedButton("Расшифровать", on_click=decrypt, icon=ft.Icons.LOCK_OPEN, color=ft.Colors.WHITE, bgcolor=ft.Colors.GREY_700)

    # Добавляем элементы на экран
    page.add(
        input_field,
        ft.Row([btn_encrypt, btn_decrypt], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
        output_field
    )

# Новый метод запуска
ft.run(main)