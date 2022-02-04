from dataclasses import field, Field
from datetime import datetime
from typing import Optional

from dataclasses_json import config
from dateutil import parser
from marshmallow import fields

from .enum import GameMode, BeatmapDifficulty


def datetime_from_iso_format(time):
    if time:
        return parser.isoparse(time)

    return None


def datetime_field(json_field_name: Optional[str] = None) -> Field:
    if json_field_name is None:
        conf = config(
                encoder=datetime.isoformat,
                decoder=datetime_from_iso_format,
                mm_field=fields.DateTime(format='iso')
            )
    else:
        conf = config(
            encoder=datetime.isoformat,
            decoder=datetime_from_iso_format,
            mm_field=fields.DateTime(format='iso'),
            field_name=json_field_name,
        )

    return field(
        default=None,
        metadata=conf
    )


def game_mode_decoder(value: any) -> GameMode:
    if GameMode.has_value(value):
        return GameMode(value)

    # Some weird "StandardHM" characteristic that doesnt exist anymore
    if "Standard" in value:
        return GameMode.STANDARD

    if GameMode.has_value(value):
        return GameMode(value)

    return GameMode.UNKNOWN


def game_mode_encoder(game_mode: GameMode) -> str:
    return game_mode.value


def game_mode_field(json_field_name: Optional[str] = None) -> Field:
    return field(
        default=None,
        metadata=config(
            encoder=game_mode_encoder,
            decoder=game_mode_decoder,
            field_name=json_field_name
        )
    )


def difficulty_decoder(value: any) -> BeatmapDifficulty:
    if BeatmapDifficulty.has_value(value):
        return BeatmapDifficulty(value)

    return BeatmapDifficulty.UNKNOWN


def difficulty_encoder(beatmap_difficulty: BeatmapDifficulty) -> int:
    return beatmap_difficulty.value


def difficulty_field(json_field_name: Optional[str] = None) -> Field:
    return field(
        default=None,
        metadata=config(
            encoder=difficulty_encoder,
            decoder=difficulty_decoder,
            field_name=json_field_name
        )
    )


def default(json_field_name: Optional[str] = None) -> Field:
    if json_field_name is None:
        conf = config()
    else:
        conf = config(field_name=json_field_name)

    return field(
        default=None,
        metadata=conf
    )
