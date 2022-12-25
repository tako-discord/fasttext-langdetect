import pytest
from unittest import TestCase
from ftlangdetect import detect

pytest_plugins = ('pytest_asyncio',)

class TestDetect(TestCase):

    @pytest.mark.asyncio
    async def test_detect_low_mem(self):
        result = await detect("Bugün hava çok güzel", low_memory=True)
        assert "lang" in result
        assert "score" in result
        assert isinstance(result["lang"], str)
        assert isinstance(result["score"], float)
        
    @pytest.mark.asyncio
    async def test_detect_high_mem(self):
        result = await detect("Bugün hava çok güzel", low_memory=False)
        assert "lang" in result
        assert "score" in result
        assert isinstance(result["lang"], str)
        assert isinstance(result["score"], float)
