import asyncio
from typing import TextIO

import click

from sensor.cli.protoc import protoc as _protoc
from sensor.cli.serve import serve as _serve
from sensor.cli.serve import serve_witout_ssl as _serve_without_ssl
from sensor.cli.types import SENSOR_VARIANT
from sensor.types import ReadSensor


@click.group()
def cli() -> None:
    ...


@cli.command()
def protoc() -> None:
    _protoc()


@cli.command()
@click.option("--port", default=5000, show_default=True)
@click.option("--variant", type=SENSOR_VARIANT, default="fake", show_default=True)
@click.option("--ssl-certificate", type=click.File(), required=True)
@click.option("--ssl-private-key", type=click.File(), required=True)
@click.option("--ssl-root-certificate", type=click.File())
def serve(
    port: int,
    variant: ReadSensor,
    ssl_certificate: TextIO,
    ssl_private_key: TextIO,
    ssl_root_certificate: TextIO | None,
) -> None:
    serve_coroutine = _serve(
        port,
        variant,
        ssl_certificate=ssl_certificate.read(),
        ssl_private_key=ssl_private_key.read(),
        ssl_root_certificate=ssl_certificate.read()
        if ssl_root_certificate is not None
        else None,
    )

    asyncio.run(serve_coroutine)


@cli.command()
@click.option("--port", default=5000, show_default=True)
@click.option("--variant", type=SENSOR_VARIANT, default="fake", show_default=True)
def serve_without_ssl(port: int, variant: ReadSensor) -> None:
    asyncio.run(_serve_without_ssl(port, variant))
