import tkinter as tk
from tkinter import ttk, messagebox
import json
import random
from datetime import datetime, timedelta
import math

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.weather_data = []
        self.current_city = "Auckland, New Zealand"
        
        # Apple-style colors
        self.colors = {
            'bg': '#f5f5f7',
            'card_bg': '#ffffff',
            'primary': '#007aff',
            'secondary': '#5856d6',
            'text_primary': '#1d1d1f',
            'text_secondary': '#86868b',
            'accent': '#30d158',
            'warning': '#ff9500',
            'shadow': '#00000010'
        }
        
        self.create_widgets()
        self.generate_sample_data()
        self.update_display()
        
    def setup_window(self):
        self.root.title("Weather Analytics")
        self.root.geometry("900x700")
        self.root.configure(bg='#f5f5f7')
        self.root.resizable(True, True)
        
        # Center window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (900 // 2)
        y = (self.root.winfo_screenheight() // 2) - (700 // 2)
        self.root.geometry(f"900x700+{x}+{y}")
        
    def create_card_frame(self, parent, **kwargs):
        """Create Apple-style card frame"""
        frame = tk.Frame(parent, bg=self.colors['card_bg'], relief='flat', bd=0, **kwargs)
        # Add subtle shadow effect with borders
        shadow_frame = tk.Frame(parent, bg='#e5e5e7', height=2)
        return frame
        
    def create_widgets(self):
        # Main container with padding
        main_container = tk.Frame(self.root, bg=self.colors['bg'])
        main_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Header
        self.create_header(main_container)
        
        # Content area with grid layout
        content_frame = tk.Frame(main_container, bg=self.colors['bg'])
        content_frame.pack(fill='both', expand=True, pady=(20, 0))
        
        # Configure grid weights
        content_frame.grid_rowconfigure(1, weight=1)
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_columnconfigure(1, weight=1)
        
        # Current weather card
        self.create_current_weather_card(content_frame)
        
        # Analytics cards
        self.create_analytics_cards(content_frame)
        
        # Controls
        self.create_controls(content_frame)
        
    def create_header(self, parent):
        header_frame = tk.Frame(parent, bg=self.colors['bg'])
        header_frame.pack(fill='x', pady=(0, 10))
        
        # App title
        title_label = tk.Label(
            header_frame,
            text="Auckland Weather Analytics",
            font=('Helvetica', 28, 'bold'),
            fg=self.colors['text_primary'],
            bg=self.colors['bg']
        )
        title_label.pack(side='left')
        
        # Current time/date
        time_label = tk.Label(
            header_frame,
            text=datetime.now().strftime("%A, %B %d"),
            font=('Helvetica', 14),
            fg=self.colors['text_secondary'],
            bg=self.colors['bg']
        )
        time_label.pack(side='right')
        
    def create_current_weather_card(self, parent):
        # Current weather - full width card
        current_card = self.create_card_frame(parent, padx=20, pady=20)
        current_card.grid(row=0, column=0, columnspan=2, sticky='ew', pady=(0, 15))
        
        # Weather icon and temperature
        weather_frame = tk.Frame(current_card, bg=self.colors['card_bg'])
        weather_frame.pack(fill='x')
        
        # Left side - main info
        left_frame = tk.Frame(weather_frame, bg=self.colors['card_bg'])
        left_frame.pack(side='left', fill='both', expand=True)
        
        self.temp_label = tk.Label(
            left_frame,
            text="72°",
            font=('Helvetica', 48, 'normal'),
            fg=self.colors['text_primary'],
            bg=self.colors['card_bg']
        )
        self.temp_label.pack(anchor='w')
        
        self.condition_label = tk.Label(
            left_frame,
            text="Partly Cloudy",
            font=('Helvetica', 18),
            fg=self.colors['text_secondary'],
            bg=self.colors['card_bg']
        )
        self.condition_label.pack(anchor='w', pady=(0, 10))
        
        self.city_label = tk.Label(
            left_frame,
            text=self.current_city,
            font=('Helvetica', 16, 'bold'),
            fg=self.colors['text_primary'],
            bg=self.colors['card_bg']
        )
        self.city_label.pack(anchor='w')
        
        # Right side - details
        right_frame = tk.Frame(weather_frame, bg=self.colors['card_bg'])
        right_frame.pack(side='right', padx=(20, 0))
        
        details = [
            ("Humidity", "75%"),
            ("Wind", "12 km/h"),
            ("UV Index", "8"),
            ("Pressure", "1015 hPa")
        ]
        
        self.detail_labels = {}
        for label, value in details:
            detail_frame = tk.Frame(right_frame, bg=self.colors['card_bg'])
            detail_frame.pack(fill='x', pady=2)
            
            tk.Label(
                detail_frame,
                text=label,
                font=('Helvetica', 12),
                fg=self.colors['text_secondary'],
                bg=self.colors['card_bg']
            ).pack(side='left')
            
            self.detail_labels[label] = tk.Label(
                detail_frame,
                text=value,
                font=('Helvetica', 12, 'bold'),
                fg=self.colors['text_primary'],
                bg=self.colors['card_bg']
            )
            self.detail_labels[label].pack(side='right')
            
    def create_analytics_cards(self, parent):
        # Analytics cards in 2x2 grid
        cards_info = [
            ("7-Day Trend", self.create_trend_chart),
            ("Temperature Stats", self.create_temp_stats),
            ("Weekly Forecast", self.create_forecast),
            ("Historical Data", self.create_historical_chart)
        ]
        
        self.analytics_frames = {}
        for i, (title, create_func) in enumerate(cards_info):
            row = 1 + (i // 2)
            col = i % 2
            
            card = self.create_card_frame(parent, padx=15, pady=15)
            card.grid(row=row, column=col, sticky='nsew', padx=(0, 7.5) if col == 0 else (7.5, 0), pady=7.5)
            
            # Card title
            title_label = tk.Label(
                card,
                text=title,
                font=('Helvetica', 16, 'bold'),
                fg=self.colors['text_primary'],
                bg=self.colors['card_bg']
            )
            title_label.pack(anchor='w', pady=(0, 10))
            
            # Content frame
            content_frame = tk.Frame(card, bg=self.colors['card_bg'])
            content_frame.pack(fill='both', expand=True)
            
            self.analytics_frames[title] = content_frame
            create_func(content_frame)
            
    def create_controls(self, parent):
        # Control buttons at bottom
        control_frame = tk.Frame(parent, bg=self.colors['bg'])
        control_frame.grid(row=3, column=0, columnspan=2, pady=(20, 0))
        
        # Refresh button
        refresh_btn = tk.Button(
            control_frame,
            text="↻ Refresh Data",
            font=('Helvetica', 14, 'bold'),
            fg='white',
            bg=self.colors['primary'],
            relief='flat',
            bd=0,
            padx=20,
            pady=10,
            command=self.refresh_data
        )
        refresh_btn.pack(side='left', padx=(0, 10))
        
        # Export button
        export_btn = tk.Button(
            control_frame,
            text="📊 Export Data",
            font=('Helvetica', 14),
            fg=self.colors['primary'],
            bg=self.colors['card_bg'],
            relief='flat',
            bd=1,
            padx=20,
            pady=10,
            command=self.export_data
        )
        export_btn.pack(side='left')
        
    def create_trend_chart(self, parent):
        # Simple ASCII-style trend chart
        canvas = tk.Canvas(parent, bg=self.colors['card_bg'], height=120, highlightthickness=0)
        canvas.pack(fill='both', expand=True)
        
        # Generate trend data for Auckland
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        temps = [20, 23, 25, 24, 22, 26, 28]  # Auckland summer temps
        
        # Draw trend line
        width = 200
        height = 80
        margin = 20
        
        max_temp = max(temps)
        min_temp = min(temps)
        temp_range = max_temp - min_temp if max_temp != min_temp else 1
        
        points = []
        for i, temp in enumerate(temps):
            x = margin + (i * (width - 2 * margin) / (len(temps) - 1))
            y = margin + (max_temp - temp) * (height - 2 * margin) / temp_range
            points.extend([x, y])
            
            # Draw points
            canvas.create_oval(x-3, y-3, x+3, y+3, fill=self.colors['primary'], outline='')
            
            # Draw day labels
            canvas.create_text(x, height + 15, text=days[i], font=('Helvetica', 10), 
                             fill=self.colors['text_secondary'])
            
            # Draw temp labels
            canvas.create_text(x, y-15, text=f"{temp}°", font=('Helvetica', 9, 'bold'), 
                             fill=self.colors['text_primary'])
        
        # Draw trend line
        if len(points) >= 4:
            canvas.create_line(points, fill=self.colors['primary'], width=2, smooth=True)
            
    def create_temp_stats(self, parent):
        stats_frame = tk.Frame(parent, bg=self.colors['card_bg'])
        stats_frame.pack(fill='both', expand=True)
        
        stats = [
            ("Average", "23.2°C", self.colors['primary']),
            ("High", "28°C", self.colors['warning']),
            ("Low", "18°C", self.colors['secondary']),
            ("Feels Like", "25°C", self.colors['accent'])
        ]
        
        for i, (label, value, color) in enumerate(stats):
            stat_frame = tk.Frame(stats_frame, bg=self.colors['card_bg'])
            stat_frame.pack(fill='x', pady=5)
            
            # Color indicator
            indicator = tk.Frame(stat_frame, bg=color, width=4, height=20)
            indicator.pack(side='left', padx=(0, 10))
            
            # Labels
            info_frame = tk.Frame(stat_frame, bg=self.colors['card_bg'])
            info_frame.pack(side='left', fill='x', expand=True)
            
            tk.Label(
                info_frame,
                text=label,
                font=('Helvetica', 12),
                fg=self.colors['text_secondary'],
                bg=self.colors['card_bg']
            ).pack(anchor='w')
            
            tk.Label(
                info_frame,
                text=value,
                font=('Helvetica', 16, 'bold'),
                fg=self.colors['text_primary'],
                bg=self.colors['card_bg']
            ).pack(anchor='w')
            
    def create_forecast(self, parent):
        forecast_frame = tk.Frame(parent, bg=self.colors['card_bg'])
        forecast_frame.pack(fill='both', expand=True)
        
        # 5-day forecast for Auckland
        days = ['Today', 'Tomorrow', 'Wed', 'Thu', 'Fri']
        conditions = ['☀️', '🌤️', '🌧️', '☀️', '⛅']
        highs = [28, 26, 21, 29, 24]
        lows = [19, 20, 16, 22, 18]
        
        for i, (day, condition, high, low) in enumerate(zip(days, conditions, highs, lows)):
            day_frame = tk.Frame(forecast_frame, bg=self.colors['card_bg'])
            day_frame.pack(fill='x', pady=2)
            
            tk.Label(
                day_frame,
                text=day,
                font=('Helvetica', 11),
                fg=self.colors['text_secondary'],
                bg=self.colors['card_bg'],
                width=8
            ).pack(side='left')
            
            tk.Label(
                day_frame,
                text=condition,
                font=('Helvetica', 14),
                bg=self.colors['card_bg']
            ).pack(side='left', padx=(5, 10))
            
            tk.Label(
                day_frame,
                text=f"{high}°/{low}°C",
                font=('Helvetica', 11, 'bold'),
                fg=self.colors['text_primary'],
                bg=self.colors['card_bg']
            ).pack(side='right')
            
    def create_historical_chart(self, parent):
        chart_frame = tk.Frame(parent, bg=self.colors['card_bg'])
        chart_frame.pack(fill='both', expand=True)
        
        # Auckland monthly averages (Southern Hemisphere seasons)
        months = ['Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul']
        temps = [24, 22, 19, 16, 14, 13]  # Moving from summer to winter
        
        canvas = tk.Canvas(chart_frame, bg=self.colors['card_bg'], height=100, highlightthickness=0)
        canvas.pack(fill='both', expand=True, pady=(10, 0))
        
        bar_width = 25
        max_temp = max(temps)
        
        for i, (month, temp) in enumerate(zip(months, temps)):
            x = 20 + i * 35
            bar_height = (temp / max_temp) * 60
            y = 70 - bar_height
            
            # Draw bar
            canvas.create_rectangle(
                x, 70, x + bar_width, y,
                fill=self.colors['secondary'], outline=''
            )
            
            # Month label
            canvas.create_text(
                x + bar_width/2, 80,
                text=month,
                font=('Helvetica', 9),
                fill=self.colors['text_secondary']
            )
            
            # Temperature label
            canvas.create_text(
                x + bar_width/2, y - 8,
                text=f"{temp}°C",
                font=('Helvetica', 8, 'bold'),
                fill=self.colors['text_primary']
            )
            
    def generate_sample_data(self):
        """Generate realistic weather data for Auckland"""
        # Auckland typical temperature range (Southern Hemisphere - currently summer)
        base_temp = 22  # Summer temperature in Celsius
        
        for days_ago in range(30):
            date = datetime.now() - timedelta(days=days_ago)
            temp = base_temp + random.randint(-5, 8)  # Auckland summer range
            humidity = random.randint(60, 90)  # Auckland is quite humid
            
            conditions = ['Sunny', 'Partly Cloudy', 'Cloudy', 'Light Rain', 'Overcast']
            weights = [0.3, 0.25, 0.2, 0.15, 0.1]  # Auckland weather patterns
            condition = random.choices(conditions, weights=weights)[0]
            
            self.weather_data.append({
                'date': date.strftime('%Y-%m-%d'),
                'city': self.current_city,
                'temperature': temp,
                'humidity': humidity,
                'condition': condition
            })
            
    def update_display(self):
        """Update all display elements with current data"""
        if not self.weather_data:
            return
            
        # Update current weather
        latest = self.weather_data[0]
        self.temp_label.config(text=f"{latest['temperature']}°C")
        self.condition_label.config(text=latest['condition'])
        self.city_label.config(text="Auckland, New Zealand")
        
        # Update details with Auckland-specific data
        self.detail_labels['Humidity'].config(text=f"{latest['humidity']}%")
        self.detail_labels['Wind'].config(text=f"{random.randint(5, 20)} km/h")
        self.detail_labels['UV Index'].config(text=str(random.randint(6, 11)))  # Higher in summer
        self.detail_labels['Pressure'].config(text=f"{1013 + random.randint(-15, 15)} hPa")
        
    def refresh_data(self):
        """Refresh weather data for Auckland"""
        self.weather_data.clear()
        self.generate_sample_data()
        self.update_display()
        
        # Refresh analytics
        for title, frame in self.analytics_frames.items():
            for widget in frame.winfo_children():
                widget.destroy()
            
            if title == "7-Day Trend":
                self.create_trend_chart(frame)
            elif title == "Temperature Stats":
                self.create_temp_stats(frame)
            elif title == "Weekly Forecast":
                self.create_forecast(frame)
            elif title == "Historical Data":
                self.create_historical_chart(frame)
                
        messagebox.showinfo("Refresh Complete", "Auckland weather data updated")
        
    def export_data(self):
        """Export Auckland weather data to JSON"""
        try:
            filename = f"auckland_weather_{datetime.now().strftime('%Y%m%d')}.json"
            with open(filename, 'w') as f:
                json.dump(self.weather_data, f, indent=2)
            messagebox.showinfo("Export Complete", f"Auckland weather data exported to {filename}")
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export data: {str(e)}")

def main():
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
