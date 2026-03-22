import flet as ft
import random

# Единый алфавит, включающий русские, английские буквы, цифры, пробел и знаки препинания
ALPHABET = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюяABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 .,!?-():;\n"

def deterministic_shuffle(alphabet, seed_str):
    chars = list(alphabet)
    seed = sum(ord(c) * (i + 1) for i, c in enumerate(seed_str))
    for i in range(len(chars) - 1, 0, -1):
        seed = (seed * 1103515245 + 12345) & 0x7fffffff
        j = seed % (i + 1)
        chars[i], chars[j] = chars[j], chars[i]
    return "".join(chars)

KEYS = {
    1: "!#%&*+=/?:;~",
    2: "^$@_}{|][><\\",
    3: "*&!%?/-+()$~",
    4: "><}{][:;=+#/",
    5: "@#^&*()_+-=|"
}

VARIANTS = {}
for v_id, key in KEYS.items():
    shuffled = deterministic_shuffle(ALPHABET, key)
    VARIANTS[v_id] = {
        "key": key,
        "dict": {ALPHABET[i]: shuffled[i] for i in range(len(ALPHABET))},
        "rev_dict": {shuffled[i]: ALPHABET[i] for i in range(len(ALPHABET))}
    }

def main(page: ft.Page):
    # Настройки окна и темы
    page.title = "Encoder"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    page.scroll = ft.ScrollMode.AUTO # Добавлена прокрутка для мобилок
    
    page.window.width = 450
    page.window.height = 750

    # Верхняя панель
    page.appbar = ft.AppBar(
        title=ft.Text("Encoder", weight=ft.FontWeight.BOLD, size=22),
        center_title=True,
        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
        elevation=2
    )

    def show_toast(message, color=ft.Colors.GREEN_600):
        # В новых версиях Flet всплывающие уведомления добавляются через overlay
        snack = ft.SnackBar(ft.Text(message, size=16), bgcolor=color, duration=2000)
        page.overlay.append(snack)
        snack.open = True
        page.update()

    def encrypt(e):
        text = input_field.value
        if not text:
            return

        variant_id = random.choice(list(KEYS.keys()))
        current_var = VARIANTS[variant_id]
        key = current_var["key"]
        
        mapped_text = ""
        for char in text:
            if char in ALPHABET:
                enc_char = current_var["dict"][char]
                mapped_text += enc_char
                next_id = (ord(enc_char) % 5) + 1
                current_var = VARIANTS[next_id]
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
            show_toast("Ошибка: Здесь нет зашифрованного сообщения!", ft.Colors.ERROR)
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
            show_toast("Ошибка: Неверный ключ или текст поврежден.", ft.Colors.ERROR)
            return

        decrypted_result = ""
        current_var = active_variant
        
        for char in clean_text:
            if char in ALPHABET:
                dec_char = current_var["rev_dict"][char]
                decrypted_result += dec_char
                next_id = (ord(char) % 5) + 1
                current_var = VARIANTS[next_id]
            else:
                decrypted_result += char

        output_field.value = decrypted_result
        page.update()

    # --- Функции для новых кнопок ---
    def copy_result(e):
        if output_field.value:
            # Новый API для буфера обмена
            page.clipboard.set(output_field.value)
            show_toast("Результат скопирован в буфер!")

    def copy_input(e):
        if input_field.value:
            # Новый API для буфера обмена
            page.clipboard.set(input_field.value)
            show_toast("Исходный текст скопирован!")

    def clear_all(e):
        input_field.value = ""
        output_field.value = ""
        page.update()
        show_toast("Поля очищены", ft.Colors.BLUE_GREY_600)

    # --- UI Элементы ---

    # Стилизованные поля ввода
    input_field = ft.TextField(
        multiline=True, 
        min_lines=5, 
        max_lines=7, 
        text_size=16,
        hint_text="Введите текст для шифрования или дешифровки...",
        border_radius=12,
        border_color=ft.Colors.TRANSPARENT,
        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
        content_padding=15
    )
    
    output_field = ft.TextField(
        multiline=True, 
        min_lines=5, 
        max_lines=7, 
        text_size=16,
        hint_text="Здесь появится результат...",
        border_radius=12,
        border_color=ft.Colors.TRANSPARENT,
        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
        content_padding=15,
        read_only=True # Запрещаем редактировать вывод
    )
    
    # Кнопки действия (заменены устаревшие ElevatedButton на современные Button)
    btn_encrypt = ft.Button(
        "Зашифровать", 
        on_click=encrypt, 
        icon=ft.Icons.LOCK, 
        style=ft.ButtonStyle(
            color=ft.Colors.WHITE, 
            bgcolor=ft.Colors.BLUE_700,
            shape=ft.RoundedRectangleBorder(radius=10), 
            padding=15
        )
    )
    
    btn_decrypt = ft.Button(
        "Расшифровать", 
        on_click=decrypt, 
        icon=ft.Icons.LOCK_OPEN, 
        style=ft.ButtonStyle(
            color=ft.Colors.WHITE, 
            bgcolor=ft.Colors.GREY_800,
            shape=ft.RoundedRectangleBorder(radius=10), 
            padding=15
        )
    )

    # --- Сборка интерфейса на экране ---
    page.add(
        # Блок ввода с иконками
        ft.Row([
                ft.Text("Исходный текст", size=18, weight=ft.FontWeight.W_600),
                ft.Row([
                    ft.IconButton(icon=ft.Icons.COPY, tooltip="Скопировать ввод", on_click=copy_input, icon_size=20),
                    ft.IconButton(icon=ft.Icons.DELETE_SWEEP, tooltip="Очистить всё", on_click=clear_all, icon_size=22, icon_color=ft.Colors.RED_400),
                ], spacing=0)
            ], 
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        ),
        input_field,
        
        # Центрированный блок с главными кнопками (исправлен margin)
        ft.Container(
            content=ft.Row([btn_encrypt, btn_decrypt], alignment=ft.MainAxisAlignment.CENTER, spacing=15),
            margin=ft.Margin.symmetric(vertical=15)
        ),

        # Блок вывода с иконкой копирования
        ft.Row([
                ft.Text("Результат", size=18, weight=ft.FontWeight.W_600),
                ft.IconButton(icon=ft.Icons.COPY, tooltip="Скопировать результат", on_click=copy_result, icon_size=20, icon_color=ft.Colors.BLUE_400)
            ], 
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        ),
        output_field
    )

ft.run(main)