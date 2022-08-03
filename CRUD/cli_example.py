import click

@click.group()
def main():
    pass

@main.command()
def saluda_usuarios():
    print('hola mundo')


@main.command()
def despedida_usuarios():
    print('hola mundo')
    
