main.py
import typer
import json
import os
from rich.console import Console
from rich.table import Table
from rich import box
from datetime import datetime

# Uygulama ve Konsol Ayarları
app = typer.Typer()
console = Console()
DATA_FILE = "tasks.json"

# Veri Yükleme Fonksiyonu
def load_tasks():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

# Veri Kaydetme Fonksiyonu
def save_tasks(tasks):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=4, ensure_ascii=False)

@app.command()
def add(task: str, category: str = "Genel"):
    """Yeni bir görev ekler. Örnek: python main.py add 'Python Çalış' --category 'Yazılım'"""
    tasks = load_tasks()
    new_task = {
        "id": len(tasks) + 1,
        "task": task,
        "category": category,
        "status": "Bekliyor",
        "date": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    tasks.append(new_task)
    save_tasks(tasks)
    console.print(f"[bold green]✔ Görev Başarıyla Eklendi:[/bold green] {task}")

@app.command()
def list():
    """Mevcut tüm görevleri estetik bir tabloda listeler."""
    tasks = load_tasks()
    if not tasks:
        console.print("[bold red]✖ Hiç kayıtlı görev yok![/bold red]")
        return

    table = Table(title="🚀 Görev Listesi", box=box.ROUNDED, header_style="bold cyan")
    table.add_column("ID", justify="center", style="dim")
    table.add_column("Görev", style="bold white")
    table.add_column("Kategori", style="magenta")
    table.add_column("Durum", justify="center")
    table.add_column("Tarih", justify="right", style="green")

    for t in tasks:
        status_icon = "✅" if t["status"] == "Tamamlandı" else "⏳"
        status_style = "green" if t["status"] == "Tamamlandı" else "yellow"
        table.add_row(
            str(t["id"]), 
            t["task"], 
            t["category"], 
            f"[{status_style}]{status_icon} {t['status']}[/{status_style}]", 
            t["date"]
        )

    console.print(table)

@app.command()
def complete(task_id: int):
    """Bir görevi tamamlandı olarak işaretler."""
    tasks = load_tasks()
    found = False
    for t in tasks:
        if t["id"] == task_id:
            t["status"] = "Tamamlandı"
            found = True
            break
    
    if found:
        save_tasks(tasks)
        console.print(f"[bold green]✨ Görev #{task_id} tamamlandı![/bold green]")
    else:
        console.print(f"[bold red]✖ Görev #{task_id} bulunamadı![/bold red]")

@app.command()
def delete(task_id: int):
    """Bir görevi listeden siler."""
    tasks = load_tasks()
    new_tasks = [t for t in tasks if t["id"] != task_id]
    
    if len(tasks) == len(new_tasks):
        console.print(f"[bold red]✖ Görev #{task_id} bulunamadı![/bold red]")
    else:
        # ID'leri yeniden düzenle
        for index, task in enumerate(new_tasks):
            task["id"] = index + 1
        save_tasks(new_tasks)
        console.print(f"[bold red]🗑 Görev #{task_id} silindi.[/bold red]")

if __name__ == "__main__":
    app()
