import click
import requests

# URL base da API
API_URL = "http://localhost:8000"

@click.group()
def cli():
    """AI Programming Assistant CLI"""
    pass

@cli.command()
@click.option("--username", prompt=True, help="Nome de usuário")
@click.option("--password", prompt=True, hide_input=True, help="Senha")
def register(username, password):
    """Registra um novo usuário."""
    try:
        response = requests.post(
            f"{API_URL}/register",
            json={"username": username, "password": password}
        )
        response.raise_for_status()
        click.echo(click.style("✅ Usuário registrado com sucesso!", fg="green"))
    except requests.exceptions.RequestException as e:
        click.echo(click.style(f"❌ Erro ao registrar usuário: {e}", fg="red"))

@cli.command()
@click.option("--username", prompt=True, help="Nome de usuário")
@click.option("--password", prompt=True, hide_input=True, help="Senha")
def login(username, password):
    """Faz login e obtém um token de acesso."""
    try:
        response = requests.post(
            f"{API_URL}/token",
            data={"username": username, "password": password}
        )
        response.raise_for_status()
        token = response.json().get("access_token")
        click.echo(click.style("✅ Login realizado com sucesso!", fg="green"))
        click.echo(click.style(f"Token: {token}", fg="blue"))
    except requests.exceptions.RequestException as e:
        click.echo(click.style(f"❌ Erro ao fazer login: {e}", fg="red"))

@cli.command()
@click.option("--token", prompt=True, help="Token de acesso")
@click.option("--prompt", prompt=True, help="Prompt para a IA")
def ask(token, prompt):
    """Envia um prompt para a IA."""
    try:
        response = requests.post(
            f"{API_URL}/analyze",
            headers={"Authorization": f"Bearer {token}"},
            json={"code": prompt}
        )
        response.raise_for_status()
        result = response.json()
        click.echo(click.style("🤖 Resposta da IA:", fg="blue"))
        click.echo(result.get("analysis"))
    except requests.exceptions.RequestException as e:
        click.echo(click.style(f"❌ Erro ao enviar prompt: {e}", fg="red"))

if __name__ == "__main__":
    cli()