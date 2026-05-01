"""프로젝트 경로 + API key 로딩 (모든 script 공통)"""
from pathlib import Path
import os
from dotenv import load_dotenv


# 프로젝트 root: 이 파일 기준 ../../..
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# .env 로드
load_dotenv(PROJECT_ROOT / ".env")

# 경로
RAW_DIR = PROJECT_ROOT / "0_raw"
CODEBOOKS_DIR = PROJECT_ROOT / "1_codebooks"
SCRIPTS_DIR = PROJECT_ROOT / "2_scripts"
DERIVED_DIR = PROJECT_ROOT / "3_derived"
RESULTS_DIR = PROJECT_ROOT / "4_results"
LOGS_DIR = PROJECT_ROOT / "5_logs"
PIPELINE_LOGS_DIR = LOGS_DIR / "pipeline_runs"
DECISIONS_DIR = LOGS_DIR / "decisions"

# API keys
ECOS_API_KEY = os.environ.get("ECOS_API_KEY", "")
COMTRADE_API_KEY = os.environ.get("COMTRADE_API_KEY", "")
COMTRADE_API_KEY_SECONDARY = os.environ.get("COMTRADE_API_KEY_SECONDARY", "")
COMTRADE_API_KEY_TERTIARY = os.environ.get("COMTRADE_API_KEY_TERTIARY", "")
COMTRADE_API_KEY_QUATERNARY = os.environ.get("COMTRADE_API_KEY_QUATERNARY", "")
DATA_GO_KR_API_KEY = os.environ.get("DATA_GO_KR_API_KEY", "")
KOSIS_API_KEY = os.environ.get("KOSIS_API_KEY", "")

# Comtrade key pool — 빈 키 자동 제외하고 round-robin 가능한 리스트
COMTRADE_KEYS = [k for k in (
    COMTRADE_API_KEY,
    COMTRADE_API_KEY_SECONDARY,
    COMTRADE_API_KEY_TERTIARY,
    COMTRADE_API_KEY_QUATERNARY,
) if k]


def assert_api_key(name: str, key: str) -> None:
    if not key:
        raise RuntimeError(
            f"{name} API key 가 .env 에 없습니다. .env.example 참조."
        )


if __name__ == "__main__":
    print(f"PROJECT_ROOT = {PROJECT_ROOT}")
    print(f"RAW_DIR exists: {RAW_DIR.exists()}")
    print(f"ECOS key set: {bool(ECOS_API_KEY)}")
    print(f"COMTRADE key set: {bool(COMTRADE_API_KEY)}")
    print(f"DATA_GO_KR key set: {bool(DATA_GO_KR_API_KEY)}")
