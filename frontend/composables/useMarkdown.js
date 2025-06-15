import { marked } from 'marked'
import { markedHighlight } from 'marked-highlight'
import hljs from 'highlight.js'
import 'highlight.js/styles/atom-one-dark.css'

// Configure marked with the highlight extension
marked.use(markedHighlight({
  langPrefix: 'hljs language-',
  highlight(code, lang) {
    console.log('Highlighting code with language:', lang)
    
    const language = hljs.getLanguage(lang) ? lang : 'plaintext'
    const result = hljs.highlight(code, { language }).value
    console.log('Highlighted result:', result.substring(0, 100))
    return result
  }
}))

// Configure other marked options
marked.use({
  breaks: true,
  gfm: true,
})

export const useMarkdown = () => {
  const renderMarkdown = (markdown, options = {}) => {
    if (!markdown) return ''
    
    try {
      let result = marked.parse(markdown)
      console.log('Markdown parsed, result length:', result.length)
      
      // If we need to append typing indicator, add it to the last text element
      if (options.appendTypingIndicator) {
        // Find the last closing tag before </p>, </li>, or end of content
        const lastParagraphMatch = result.match(/(.*)<\/p>\s*$/s)
        const lastListItemMatch = result.match(/(.*)<\/li>\s*<\/[uo]l>\s*$/s)
        
        if (lastParagraphMatch) {
          // Append to last paragraph
          result = result.replace(/<\/p>\s*$/s, '<span class="typing-indicator">▌</span></p>')
        } else if (lastListItemMatch) {
          // Append to last list item
          result = result.replace(/<\/li>\s*(<\/[uo]l>\s*)$/s, '<span class="typing-indicator">▌</span></li>$1')
        } else {
          // If no paragraph or list, append at the end
          result = result.trimEnd() + '<span class="typing-indicator">▌</span>'
        }
      }
      
      return result
    } catch (error) {
      console.error('Error parsing markdown:', error)
      return markdown
    }
  }

  return {
    renderMarkdown
  }
}