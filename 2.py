import pandas as pd
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class CalorieCounter:
    def __init__(self, excel_file, save_file):
        self.food_data = pd.read_excel(excel_file)
        self.consumed_food = []
        self.total_calories = 0
        self.save_file = save_file

        self.load_data()

    def add_food(self, food_name, quantity):
        food_entry = self.food_data[self.food_data['Product'] == food_name]
        if not food_entry.empty:
            calories = food_entry['Calories'].values[0] * quantity
            self.total_calories += calories
            self.consumed_food.append({'product': food_name, 'calories': calories, 'quantity': quantity})
            self.update_consumed_food_list()
            self.update_visualization()
            total_calories_text.set(self.total_calories)
            self.save_data()
        else:
            result_text.set(f"Продукт '{food_name}' не найден в базе данных")

    def add_food(self, food_name, quantity):
        food_entry = self.food_data[self.food_data['Product'] == food_name]
        if not food_entry.empty:
            calories = food_entry['Calories'].values[0] * quantity

            # Check if the food item already exists in the consumed_food list
            existing_food = next((food for food in self.consumed_food if food['product'] == food_name), None)

            if existing_food:
                # Update the quantity and calories of the existing food item
                existing_food['quantity'] += quantity
                existing_food['calories'] += calories
            else:
                # Add a new entry for the food item
                self.consumed_food.append({'product': food_name, 'calories': calories, 'quantity': quantity})

            self.total_calories += calories
            self.update_consumed_food_list()
            self.update_visualization()
            total_calories_text.set(self.total_calories)
            self.save_data()
        else:
            result_text.set(f"Продукт '{food_name}' не найден в базе данных")

    def remove_food(self, index):
        if index < len(self.consumed_food):
            removed_food = self.consumed_food.pop(index)
            self.total_calories -= removed_food['calories']
            self.update_consumed_food_list()
            self.update_visualization()
            total_calories_text.set(self.total_calories)
            self.save_data()


    def update_consumed_food_list(self):
        consumed_food_text.delete(0, tk.END)
        consumed_calories_text.delete(0, tk.END)
        for food in self.consumed_food:
            consumed_food_text.insert(tk.END, f"{food['product']} ({food['quantity']})\n")
            consumed_calories_text.insert(tk.END, f"{food['calories']}\n")

    def update_visualization(self):
        products = [food['product'] for food in self.consumed_food]
        calories = [food['calories'] for food in self.consumed_food]

        fig, ax = plt.subplots(figsize=(6, 4))
        ax.bar(products, calories)
        ax.set_xlabel('Продукты')
        ax.set_ylabel('Калории')
        ax.set_title('Потребленные продукты и калории')
        ax.tick_params(axis='x', rotation=45)
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=visualization_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0, sticky='nsew')

    def save_data(self):
        data = {
            'consumed_food': self.consumed_food,
            'total_calories': self.total_calories
        }
        pd.DataFrame(data).to_csv(self.save_file, index=False)

    def load_data(self):
        try:
            data = pd.read_csv(self.save_file)
            self.consumed_food = data['consumed_food'].tolist()
            self.total_calories = data['total_calories'].values[0]
            self.update_consumed_food_list()
            self.update_visualization()
            total_calories_text.set(self.total_calories)
        except FileNotFoundError:
            pass

def add_food_button_click():
    food_name = food_entry.get()
    quantity = int(quantity_entry.get())
    counter.add_food(food_name, quantity)
    food_entry.delete(0, tk.END)
    quantity_entry.delete(0, tk.END)


def remove_food_button_click():
    selected_indices = consumed_food_text.curselection()
    if selected_indices:
        index = int(selected_indices[0])
        counter.remove_food(index)

def exit_button_click():
    counter.save_data()
    window.destroy()

excel_file = "food_data.xlsx"  # Путь к файлу Excel с данными о продуктах и калориях
save_file = "consumed_data.csv"  # Путь к файлу для сохранения данных о потребленных продуктах и калориях
counter = CalorieCounter(excel_file, save_file)

window = tk.Tk()
window.title("Счетчик калорий")

main_frame = ttk.Frame(window, padding="20")
main_frame.pack()

food_label = ttk.Label(main_frame, text="Введите название продукта:")
food_label.grid(row=0, column=0, sticky='w')

food_entry = ttk.Entry(main_frame)
food_entry.grid(row=1, column=0, sticky='we')

quantity_label = ttk.Label(main_frame, text="Введите количество:")
quantity_label.grid(row=2, column=0, sticky='w')

quantity_entry = ttk.Entry(main_frame)
quantity_entry.grid(row=3, column=0, sticky='we')

add_food_button = ttk.Button(main_frame, text="Добавить продукт", command=add_food_button_click)
add_food_button.grid(row=4, column=0, sticky='we')

consumed_frame = ttk.Frame(main_frame, padding="10")
consumed_frame.grid(row=5, column=0, sticky='nsew')

consumed_food_label = ttk.Label(consumed_frame, text="Употребленные продукты:")
consumed_food_label.grid(row=0, column=0, sticky='w')

consumed_calories_label = ttk.Label(consumed_frame, text="Калории:")
consumed_calories_label.grid(row=0, column=1, sticky='w')

consumed_food_text = tk.Listbox(consumed_frame, width=30, height=10)
consumed_food_text.grid(row=1, column=0, sticky='nsew')

consumed_calories_text = tk.Listbox(consumed_frame, width=10, height=10)
consumed_calories_text.grid(row=1, column=1, sticky='nsew')

visualization_frame = ttk.Frame(main_frame, padding="10")
visualization_frame.grid(row=6, column=0, sticky='nsew')

remove_food_button = ttk.Button(main_frame, text="Удалить продукт", command=remove_food_button_click)
remove_food_button.grid(row=7, column=0, sticky='we')

total_calories_label = ttk.Label(main_frame, text="Общая сумма калорий:")
total_calories_label.grid(row=8, column=0, sticky='w')

total_calories_text = tk.StringVar()
total_calories_value = ttk.Label(main_frame, textvariable=total_calories_text)
total_calories_value.grid(row=9, column=0, sticky='w')

exit_button = ttk.Button(main_frame, text="Выход", command=exit_button_click)
exit_button.grid(row=10, column=0, sticky='we')

result_text = tk.StringVar()
result_label = ttk.Label(main_frame, textvariable=result_text, foreground='red')
result_label.grid(row=11, column=0, sticky='w')

window.columnconfigure(0, weight=1)
window.rowconfigure(0, weight=1)
main_frame.columnconfigure(0, weight=1)
main_frame.rowconfigure(5, weight=1)

window.mainloop()
