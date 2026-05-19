-- Custom title slide filter for Quarto reveal.js
-- Injects affiliation, event, and date into title slide

function Pandoc(doc)
  local meta = doc.meta
  local title_slide = nil
  
  -- Find the title slide section
  for i, el in ipairs(doc.blocks) do
    if el.attr and el.attr.id == "title-slide" then
      title_slide = el
      break
    end
  end
  
  if title_slide then
    local author = meta.author
    local affiliation = meta.affiliation
    local event = meta.event
    local date = meta.date
    
    -- Build content for title slide author section
    local author_content = {}
    
    if author then
      if type(author) == "table" and author[1] then
        table.insert(author_content, pandoc.Para(author[1]))
      elseif type(author) == "string" then
        table.insert(author_content, pandoc.Para(pandoc.Str(author)))
      end
    end
    
    if affiliation then
      if type(affiliation) == "table" and affiliation[1] then
        table.insert(author_content, pandoc.Para(affiliation[1]))
      else
        table.insert(author_content, pandoc.Para(pandoc.Str(tostring(affiliation))))
      end
    end
    
    if event then
      if type(event) == "table" and event[1] then
        table.insert(author_content, pandoc.Para(event[1]))
      else
        table.insert(author_content, pandoc.Para(pandoc.Str(tostring(event))))
      end
    end
    
    if date then
      if type(date) == "table" and date[1] then
        table.insert(author_content, pandoc.Para(date[1]))
      else
        table.insert(author_content, pandoc.Para(pandoc.Str(tostring(date))))
      end
    end
    
    -- Append to title slide if we have content
    if #author_content > 0 then
      for _, para in ipairs(author_content) do
        table.insert(title_slide.content, para)
      end
    end
  end
  
  return doc
end
