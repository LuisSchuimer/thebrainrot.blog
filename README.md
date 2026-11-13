# The Brainrot Blog
## Posts
**ToDo List**
- create database construct
  - Field names
    - id: str
    - title: str
    - rendered html: str (cache)
    - core markdown byte size or char count (to check if something changed): int
- create article list view
- implement a way to upload new posts to server over admin page
- search algorithm to search for posts or certain keywords (database table for those)?

## Renderer
**ToDo List**
- [x] ~~Envision a new system for actively and elegantly render to html code~~
    -  [x] **Tree search** (only implemented in parser tests) maybe optimise (O(log n) to O(n)?)
      - Indexes of included lines or open styles are located as a key value
      - Iterate over those indexes to find ruff location and repeat until exact index is found
        - Save those included lines and remember so that another search is not needed
        - -> *Should be o(log n) or (idealy) o(n)*
- [x] ~~Build core tree structure~~
- [x] Write tests for tree structure **(3 tests implemented -> more to come)**
- [x] ~~Think about data structures for new handler_config file~~
- [ ] **Make code more elegant and fast** -> Look at new render system structure
- Add support for more styling types
  - [x] Highlight (==)
  - [x] Strikethrough (~~) 
  - [x] Blockquote (>)
  - [x] Bold
  - [x] Italic
  - [x] Highlight
  - [ ] Horisontal rules
  - [ ] Task lists
  - [ ] URLS
  - [ ] Hrefs 
  - [x] Title sizes from 4-6
  - [ ] Links inside document
- [ ] Add tests for renderer
## Parser
**ToDo List**
- [x] ~~Write tests for **specific styling recogniton**~~
- [x] ~~**Write function to relyably detect index changes** in styling and change them based on deleted content f.e. specific styling patterns~~
  - *Is such a function even nessersary?*
- Implement more specific styling patterns
  - [x] Highlight (==)
  - [x] Strikethrough (~~) 
  - [x] Horisontal rules
  - [ ] Multi Bullet point 
  - [ ] Images
  - [x] Task lists
  - [x] URLS
  - [x] Hrefs 
  - [x] Title sizes from 4-6
  - [x] Links inside document
- Implement more options for styling
  - [x] Title ids (links in document still to be done)
- [x] ~~Rethink the **specific styling detection system** for code reduction~~
- [x] ~~Add a way to change **indexes of found styling patterns** to still be correct~~
- [ ] Implement regex groups for better detection for images and links (**Partly done**)
- [x] ~~Better detection implementation for hrefs and regex for url~~
- [x] ~~Fix not 100% supported tasklists (like in markdown) after better implementation for hrefs~~
- [x] ~~Write global id stack for article wide title ids~~
- [ ] Fix horisontal rules not obeying the rules of markdown syntax