

class Formater:
    @staticmethod
    def format_money(value: float):
        return f"{value:,.0f} ₽".replace(",", " ")
    @staticmethod
    def format_int(value: int | float):
        return f"{int(value):,}".replace(",", " ")
    @staticmethod
    def format_float(value: float, digits=2):
        return f"{value:.{digits}f}"
    @staticmethod
    def format_minutes(value: float):
        return f"{round(value)} мин"
    
formater = Formater()