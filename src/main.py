import click


@click.command()
@click.option('--line-webhook', 'webhook', prompt=True, help='LINE webhook.')
def main(webhook: str) -> None:
    pass


if __name__ == "__main__":
    main()
