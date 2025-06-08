from playwright.async_api import async_playwright
from typing import Optional
import asyncio
from convertors.wrappers import JSXConverter

class PlaywrightManager:
    _instance = None
    _browser = None
    _initialized = False
    
    # Tailwind CSS CDN script
    TAILWIND_CSS = """
    <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
    """

    @classmethod
    async def get_instance(cls):
        if not cls._instance:
            cls._instance = cls()
            await cls._instance.initialize()
        return cls._instance

    async def initialize(self):
        if not self._initialized:
            self._playwright = await async_playwright().start()
            self._browser = await self._playwright.chromium.launch(
                headless=True
            )
            self._initialized = True

    def _prepare_html_content(self, content: str, context: dict = None, is_jsx: bool = False) -> str:
        # Convert JSX to HTML if needed
        is_jsx = True
        if is_jsx:
            content = JSXConverter().convert(content, context)

        # Wrap content with proper HTML structure and Tailwind
        return f"""
        <!DOCTYPE html>
        <html>
            <head>
                <meta charset="UTF-8" />
                <meta name="viewport" content="width=device-width, initial-scale=1.0" />
                <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
                <style type="text/tailwindcss">
                
    </style>
            </head>
            <body>
                {content}
            </body>
        </html>
        """

    async def generate_pdf(self, content: str, context: dict = None, is_jsx: bool = False) -> bytes:
        if not self._initialized:
            await self.initialize()
            
        page = await self._browser.new_page()
        try:
            html_content = self._prepare_html_content(content, context, is_jsx)
            await page.set_content(html_content)
            # Wait for Tailwind to initialize
            await page.wait_for_load_state("networkidle")
            pdf_bytes = await page.pdf(format="A4")
            return pdf_bytes
        finally:
            await page.close()

    async def cleanup(self):
        if self._browser:
            await self._browser.close()
        if hasattr(self, '_playwright'):
            await self._playwright.stop()
        self._initialized = False 

