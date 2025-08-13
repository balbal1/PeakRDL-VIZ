      /table
         \viz_js
            box: {width: {{width}}, height:{{header_height}}, rx:15, ry:15, fill:"#aaaaaa"},
            where: {left: {{left}}, top: {{top}}}
         /number[50:0]
            \viz_js
               box: {strokeWidth: 0},
               init() {
                  let ret = {}
                  let n = this.getIndex("number") + ""
                  ret.num = new fabric.Text(n, {
                     fontSize: {{font_size}},
                     originX: "center",
                     originY: "center",
                     fontFamily: "monospace",
                  })
                  return ret
               },
               where: {left: {{(slot_width-font_size)/2}}, top: {{(header_height - font_size)/2}}},
               layout: {left: {{spacing}}}
