from pydantic import BaseModel, Field


class Beatmap(BaseModel):
    songName: str
    songSubName: str
    songAuthorName: str
    levelAuthorName: str
    songHash: str = Field(None)
    levelId: str
    songBPM: float
    noteJumpSpeed: float
    songTimeOffset: int
    length: int
    difficulty: str
    notesCount: int
    bombsCount: int
    obstaclesCount: int
    maxScore: int
    maxRank: str
    environmentName: str



class Mod(BaseModel):
    multiplier: float
    obstacles: str
    instaFail: bool
    noFail: bool
    batteryEnergy: bool
    batteryLives: int = Field(None)
    disappearingArrows: bool
    noBombs: bool
    songSpeed: str
    songSpeedMultiplier: float
    noArrows: bool
    ghostNotes: bool
    failOnSaberClash: bool
    strictAngles: bool
    fastNotes: bool
    smallNotes: bool
    proMode: bool
    zenMode: bool


class Performance(BaseModel):
    rawScore: int
    score: int
    currentMaxScore: int
    rank: str
    passedNotes: int
    hitNotes: int
    missedNotes: int
    passedBombs: int
    hitBombs: int
    combo: int
    maxCombo: int
    multiplier: int
    multiplierProgress: float
    batteryEnergy: int = Field(None)
    softFailed: bool


class NoteCut(BaseModel):
    noteID: int
    noteType: str
    noteCutDirection: str
    noteLine: int
    noteLayer: int
    speedOK: bool
    directionOK: bool
    saberTypeOK: bool
    wasCutTooSoon: bool
    initialScore:  int = Field(None)
    finalScore:  int = Field(None)
    cutDistanceScore:  int = Field(None)
    multiplier: int
    saberSpeed: float = Field(None)
    saberType: str = Field(None)
    swingRating: float
    timeDeviation: float
    cutDirectionDeviation: float
    cutDistanceToCenter: float
    timeToNextBasicNote: float = Field(None)
