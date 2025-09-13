const fs = require('fs');

// Simple Vue template to HTML converter
function vueToHtml(vueTemplate, context = {}) {
  // Replace Vue expressions with actual values
  let html = vueTemplate;
  
  // Handle Vue interpolation syntax {{ variable }}
  html = html.replace(/\{\{\s*([^}]+)\s*\}\}/g, (match, expr) => {
    try {
      // Create a function that evaluates the expression with the context
      const func = new Function(...Object.keys(context), `return ${expr.trim()}`);
      const result = func(...Object.values(context));
      
      // Handle arrays (for v-for operations)
      if (Array.isArray(result)) {
        return result.join('');
      }
      
      return result !== undefined ? result : '';
    } catch (e) {
      console.warn(`Error evaluating expression: ${expr}`, e);
      return '';
    }
  });
  
  return html;
}

// Enhanced version that handles more complex Vue template expressions
function advancedVueToHtml(vueTemplate, context = {}) {
  // Pre-process common Vue patterns
  let processed = vueTemplate;
  
  // Handle v-for directive: <li v-for="item in items">{{ item }}</li>
  processed = processed.replace(
    /<(\w+)([^>]*?)\s+v-for\s*=\s*["']([^"']+)\s+in\s+([^"']+)["']([^>]*?)>([\s\S]*?)<\/\1>/g,
    (match, tagName, beforeAttrs, itemVar, arrayExpr, afterAttrs, content) => {
      try {
        // Get the array from context
        const getArrayFunc = new Function(...Object.keys(context), `return ${arrayExpr.trim()};`);
        const array = getArrayFunc(...Object.values(context));
        
        if (!Array.isArray(array)) return '';
        
        return array.map(item => {
          // Create a new context that includes the loop variable
          const loopContext = { ...context, [itemVar.trim()]: item };
          
          // Process the content with the loop context
          let itemContent = content;
          itemContent = itemContent.replace(/\{\{\s*([^}]+)\s*\}\}/g, (innerMatch, expr) => {
            try {
              const evalFunc = new Function(...Object.keys(loopContext), `return ${expr.trim()};`);
              return evalFunc(...Object.values(loopContext));
            } catch (e) {
              console.warn('Error in loop expression:', expr, e);
              return '';
            }
          });
          
          return `<${tagName}${beforeAttrs}${afterAttrs}>${itemContent}</${tagName}>`;
        }).join('');
      } catch (e) {
        console.warn(`Error in v-for operation: ${match}`, e);
        return '';
      }
    }
  );
  
  // Handle v-if directive: <div v-if="condition">content</div>
  processed = processed.replace(
    /<(\w+)([^>]*?)\s+v-if\s*=\s*["']([^"']+)["']([^>]*?)>([\s\S]*?)<\/\1>/g,
    (match, tagName, beforeAttrs, condition, afterAttrs, content) => {
      try {
        const func = new Function(...Object.keys(context), `
          return (${condition.trim()}) ? \`<${tagName}${beforeAttrs}${afterAttrs}>${content}</${tagName}>\` : '';
        `);
        return func(...Object.values(context));
      } catch (e) {
        console.warn(`Error in v-if: ${match}`, e);
        return '';
      }
    }
  );
  
  // Handle v-show directive: <div v-show="condition">content</div>
  processed = processed.replace(
    /<(\w+)([^>]*?)\s+v-show\s*=\s*["']([^"']+)["']([^>]*?)>([\s\S]*?)<\/\1>/g,
    (match, tagName, beforeAttrs, condition, afterAttrs, content) => {
      try {
        const func = new Function(...Object.keys(context), `
          const shouldShow = ${condition.trim()};
          const style = shouldShow ? '' : ' style="display: none;"';
          return \`<${tagName}${beforeAttrs}${afterAttrs}\${style}>${content}</${tagName}>\`;
        `);
        return func(...Object.values(context));
      } catch (e) {
        console.warn(`Error in v-show: ${match}`, e);
        return '';
      }
    }
  );
  
  // Handle v-bind:class or :class directive
  processed = processed.replace(
    /\s+(?:v-bind:class|:class)\s*=\s*["']([^"']+)["']/g,
    (match, classExpr) => {
      try {
        const func = new Function(...Object.keys(context), `
          const result = ${classExpr.trim()};
          if (typeof result === 'object' && result !== null) {
            // Handle object syntax: { 'class-name': condition }
            return ' class="' + Object.keys(result).filter(key => result[key]).join(' ') + '"';
          } else if (Array.isArray(result)) {
            // Handle array syntax: ['class1', 'class2']
            return ' class="' + result.join(' ') + '"';
          } else {
            // Handle string
            return ' class="' + result + '"';
          }
        `);
        return func(...Object.values(context));
      } catch (e) {
        console.warn(`Error in :class binding: ${match}`, e);
        return ' class=""';
      }
    }
  );
  
  // Handle v-bind:style or :style directive
  processed = processed.replace(
    /\s+(?:v-bind:style|:style)\s*=\s*["']([^"']+)["']/g,
    (match, styleExpr) => {
      try {
        const func = new Function(...Object.keys(context), `
          const result = ${styleExpr.trim()};
          if (typeof result === 'object' && result !== null) {
            // Handle object syntax: { 'color': 'red', 'font-size': '14px' }
            return ' style="' + Object.keys(result).map(key => 
              key.replace(/([A-Z])/g, '-$1').toLowerCase() + ': ' + result[key]
            ).join('; ') + '"';
          } else {
            // Handle string
            return ' style="' + result + '"';
          }
        `);
        return func(...Object.values(context));
      } catch (e) {
        console.warn(`Error in :style binding: ${match}`, e);
        return ' style=""';
      }
    }
  );
  
  // Handle remaining Vue interpolations {{ expression }}
  processed = processed.replace(/\{\{\s*([^}]+)\s*\}\}/g, (match, expr) => {
    try {
      const func = new Function(...Object.keys(context), `return ${expr.trim()}`);
      const result = func(...Object.values(context));
      return result !== undefined ? result : '';
    } catch (e) {
      console.warn(`Error evaluating: ${expr}`, e);
      return '';
    }
  });
  
  // Clean up any remaining Vue directives that weren't handled
  processed = processed.replace(/\s+v-[a-zA-Z-]+\s*=\s*["'][^"']*["']/g, '');
  
  return processed;
}

// CLI interface
if (require.main === module) {
  const args = process.argv.slice(2);
  
  if (args[0] === 'test') {
    test();
    process.exit(0);
  }
  
  if (args.length < 2) {
    console.log('Usage: node vue-converter.js <vue-template-string> <context-json>');
    console.log('       node vue-converter.js test');
    console.log('Example: node vue-converter.js "<div>{{ name }}</div>" \'{"name":"John"}\'');
    process.exit(1);
  }
  
  const vueTemplate = args[0];
  const context = JSON.parse(args[1] || '{}');
  
  const html = advancedVueToHtml(vueTemplate, context);
  console.log(html);
}

// Test the converter
function test() {
    const vueTemplate = `
        <div class="invoice">
            <h1>Invoice</h1>
            <div v-if="showHeader" class="header">
                <p>Company: {{ company.name }}</p>
                <p>Address: {{ company.address }}</p>
            </div>
            
            <table class="line-items">
                <thead>
                    <tr>
                        <th>Item</th>
                        <th>Description</th>
                        <th>Quantity</th>
                        <th>Price</th>
                        <th>Tax</th>
                        <th>Total</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="lineItem in lineItems">
                        <td>{{ lineItem.item }}</td>
                        <td>{{ lineItem.description }}</td>
                        <td>{{ lineItem.quantity }}</td>
                        <td>{{ lineItem.price }}</td>
                        <td>{{ lineItem.tax }}</td>
                        <td>{{ lineItem.total }}</td>
                    </tr>
                </tbody>
            </table>
            
            <div class="total" v-show="showTotal">
                <p>Grand Total: {{ grandTotal }}</p>
            </div>
        </div>
    `;

    const context = {
        showHeader: true,
        showTotal: true,
        company: {
            name: "Acme Corp",
            address: "123 Main St, Anytown USA"
        },
        grandTotal: "$1,219.00",
        lineItems: [
            {
                tax: "6%",
                item: "Surf Board",
                price: "$1,000",
                total: "$1,060.00",
                quantity: "1",
                description: "Rides big waves"
            },
            {
                tax: "6%",
                item: "Board Wax",
                price: "$75",
                total: "$159.00",
                quantity: "2",
                description: "Best wax in town"
            }
        ]
    };

    console.log(advancedVueToHtml(vueTemplate, context));
}

// Test function is now accessible via the CLI

module.exports = { vueToHtml, advancedVueToHtml };
