from nicegui import ui

def chart_card(title: str=None):
    return ui.card().classes(
        """
        bg-[#101923]/90
        border border-[#1f2937]
        rounded-xl
        shadow-xl
        p-4
        text-white
        h-[380px]
        """
    )