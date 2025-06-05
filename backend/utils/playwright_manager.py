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

    def _prepare_html_content(self, content: str, is_jsx: bool = False) -> str:
        # Convert JSX to HTML if needed
        if is_jsx:
            content = JSXConverter().convert(content)

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
                <div class="container border-t-4 border-yellow-500">
                    <h1 class="text-3xl font-bold underline text-clifford">
                        Hello world!
                    </h1>
                </div>
                <div class="container border-t-4 border-yellow-500">
                <div class="flex flex-row justify-between my-6">
                <div class="flex">
                    <img src="https://res.cloudinary.com/dkpz9r2q7/image/upload/v1673288813/surfsup_scqki2.png" class="h-20"/>
                    <div class="ml-4">
                    <p class="text-3xl mb-2">Invoice</p>
                    <p class="text-xl">8547</p>
                    </div>
                </div>
                <div class="text-right text-gray-700">
                    <p class="text-lg font-bold text-gray-800">Surfsup</p>
                    <p>2578 Palm Tree Way</p>
                    <p>Beach City, FL 30001</p>
                    <p>United States</p>
                </div>
                </div>
                <hr />
                <div class="flex flex-row justify-between my-4">
                <div>
                    <p class="uppercase text-xs text-gray-600 mb-">Bill To</p>
                    <p>customer.name</p>
                    <p>customer.address</p>
                    <p>customer.city, customer.state customer.zip</p>
                    <p>customer.country</p>
                </div>
                <div class="text-right">
                    <div class="mb-2">
                    <p class="uppercase text-xs text-gray-600">Invoice </p>
                    <p>invoiceNumber</p>
                    </div>
                    <div class="mb-2">
                    <p class="uppercase text-xs text-gray-600">Date</p>
                    <p>date</p>
                    </div>
                    <div class="mb-2">
                    <p class="uppercase text-xs text-gray-600">Due Date</p>
                    <p>dueDate</p>
                    </div>
                </div>
                </div>
                <hr />
                <table class="min-w-full divide-y divide-gray-300">
                <thead>
                    <tr>
                    <th class="py-3.5 pl-4 pr-3 text-left text-sm font-semibold text-gray-900 pl-0">Item</th>
                    <th class="py-3.5 px-3 text-left text-sm font-semibold text-gray-900">Description</th>
                    <th class="py-3.5 px-3 text-left text-sm font-semibold text-gray-900">Quantity</th>
                    <th class="py-3.5 px-3 text-left text-sm font-semibold text-gray-900 text-right">Price</th>
                    <th class="py-3.5 px-3 text-left text-sm font-semibold text-gray-900 text-right">Tax</th>
                    <th class="py-3.5 px-3 text-left text-sm font-semibold text-gray-900 pr-0 text-right">Amount</th>
                    </tr>
                </thead>
                <tbody class="divide-y divide-gray-200">      
                    <tr>
                        <td class="whitespace-nowrap py-4 pl-4 pr-3 text-sm font-medium text-gray-900 pl-0">lineItem.item</td>
                        <td class="whitespace-nowrap py-4 px-3 text-sm text-gray-500">lineItem.description</td>
                        <td class="whitespace-nowrap py-4 px-3 text-sm text-gray-500">lineItem.quantity</td>
                        <td class="whitespace-nowrap py-4 px-3 text-sm text-gray-500 text-right">lineItem.price</td>
                        <td class="whitespace-nowrap py-4 px-3 text-sm text-gray-500 text-right">lineItem.tax</td>
                        <td class="whitespace-nowrap py-4 px-3 text-sm text-gray-500 pr-0 text-right">lineItem.total</td>          
                    </tr>
                </tbody>
                </table>
                <div class="flex flex-row justify-between mt-20">
                <div>
                    <p class="text-gray-400 text-sm mb-2">We accept cash, check, and card</p>
                    <p class="text-gray-400 text-sm">Thanks for your business!</p>
                </div>
                <div class="text-right">
                    <p class="text-gray-600 mb-2">Total</p>
                    <p class="text-4xl font-bold text-gray-800">invoiceTotal</p>
                </div>
                </div>
                </div>
            </body>
        </html>
        """

    async def generate_pdf(self, content: str, is_jsx: bool = False) -> bytes:
        if not self._initialized:
            await self.initialize()
            
        page = await self._browser.new_page()
        try:
            html_content = self._prepare_html_content(content, is_jsx)
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

