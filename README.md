# The Brainrot Blog
## Renderer
**ToDo List**
- [x] Envision a new system for actively and elegantly render to html code
  - **Specific styling**
    1. Goes through every char of content
    2. Looks for styling types associated **(created, ending or still active at char)**
    3. Adds char **(with html element for styling to article html)**
    4. Repeat
  - **Global styling**
    1. Go through every global styling
    2. Add needed html
    3. Close html element when line content is added
    4. Also check for blockqoutes and bullet points that are multiline, if they need to be closed
- [ ] Think about data structures for new handler_config file
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