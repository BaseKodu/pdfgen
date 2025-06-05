const fs = require('fs');

// Simple JSX to HTML converter without React
function jsxToHtml(jsx, context = {}) {
  // Replace JSX expressions with actual values
  let html = jsx;
  
  // Handle simple variable replacements {variable}
  html = html.replace(/\{([^}]+)\}/g, (match, expr) => {
    try {
      // Create a function that evaluates the expression with the context
      const func = new Function(...Object.keys(context), `return ${expr}`);
      const result = func(...Object.values(context));
      
      // Handle arrays (for map operations)
      if (Array.isArray(result)) {
        return result.join('');
      }
      
      return result !== undefined ? result : '';
    } catch (e) {
      console.warn(`Error evaluating expression: ${expr}`, e);
      return '';
    }
  });
  
  // Convert JSX attributes to HTML
  html = html.replace(/className=/g, 'class=');
  
  // Handle self-closing tags
  html = html.replace(/<(\w+)([^>]*?)\/>/g, '<$1$2></$1>');
  
  // Remove JSX fragments
  html = html.replace(/<React\.Fragment>|<\/React\.Fragment>|<>|<\/>/g, '');
  
  return html;
}

// Enhanced version that handles more complex expressions
function advancedJsxToHtml(jsx, context = {}) {
  // Pre-process common JSX patterns
  let processed = jsx;
  
  // Handle map operations: {items.map(item => `<li>${item}</li>`)}
  processed = processed.replace(
    /\{([^}]*?)\.map\(([^)]+)\)\}/g, 
    (match, arrayExpr, mapFunc) => {
      try {
        const func = new Function(...Object.keys(context), `
          const array = ${arrayExpr};
          return array.map(${mapFunc}).join('');
        `);
        return func(...Object.values(context));
      } catch (e) {
        console.warn(`Error in map operation: ${match}`, e);
        return '';
      }
    }
  );
  
  // Handle conditional rendering: {condition && <div>content</div>}
  processed = processed.replace(
    /\{([^}]*?)\s*&&\s*([^}]*?)\}/g,
    (match, condition, content) => {
      try {
        const func = new Function(...Object.keys(context), `
          return (${condition}) ? \`${content}\` : '';
        `);
        return func(...Object.values(context));
      } catch (e) {
        console.warn(`Error in conditional: ${match}`, e);
        return '';
      }
    }
  );
  
  // Handle ternary operators: {condition ? 'yes' : 'no'}
  processed = processed.replace(
    /\{([^}]*?\?[^}]*?:[^}]*?)\}/g,
    (match, ternary) => {
      try {
        const func = new Function(...Object.keys(context), `return ${ternary}`);
        return func(...Object.values(context));
      } catch (e) {
        console.warn(`Error in ternary: ${match}`, e);
        return '';
      }
    }
  );
  
  // Handle remaining simple expressions
  processed = processed.replace(/\{([^}]+)\}/g, (match, expr) => {
    try {
      const func = new Function(...Object.keys(context), `return ${expr}`);
      const result = func(...Object.values(context));
      return result !== undefined ? result : '';
    } catch (e) {
      console.warn(`Error evaluating: ${expr}`, e);
      return '';
    }
  });
  
  // Convert JSX to HTML
  processed = processed.replace(/className=/g, 'class=');
  processed = processed.replace(/<(\w+)([^>]*?)\/>/g, '<$1$2></$1>');
  processed = processed.replace(/<React\.Fragment>|<\/React\.Fragment>|<>|<\/>/g, '');
  
  return processed;
}

// CLI interface
if (require.main === module) {
  const args = process.argv.slice(2);
  
  if (args.length < 2) {
    console.log('Usage: node jsx-converter.js <jsx-string> <context-json>');
    console.log('Example: node jsx-converter.js "<div>{name}</div>" \'{"name":"John"}\'');
    process.exit(1);
  }
  
  const jsx = args[0];
  const context = JSON.parse(args[1] || '{}');
  
  const html = advancedJsxToHtml(jsx, context);
  console.log(html);
}

module.exports = { jsxToHtml, advancedJsxToHtml };