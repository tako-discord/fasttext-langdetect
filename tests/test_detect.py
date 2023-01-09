import pytest
from ftlangdetect import detect

pytest_plugins = ('pytest_asyncio',)

@pytest.mark.asyncio
async def test_detect_low_mem():
    result = await detect("Bugün hava çok güzel", low_memory=True)
    assert "lang" in result
    assert "score" in result
    assert isinstance(result["lang"], str)
    assert isinstance(result["score"], float)
    
@pytest.mark.asyncio
async def test_detect_high_mem():
    result = await detect("Bugün hava çok güzel", low_memory=False)
    assert "lang" in result
    assert "score" in result
    assert isinstance(result["lang"], str)
    assert isinstance(result["score"], float)
