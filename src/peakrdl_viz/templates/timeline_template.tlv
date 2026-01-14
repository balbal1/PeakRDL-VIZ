      /table
         \viz_js
            box: {width: {{timeline.width}}, height:{{timeline.header_height}}, rx:15, ry:15, fill:"#aaaaaa"},
            where: {left: {{timeline.left}}, top: {{timeline.top}}}
         /number[50:0]
            \viz_js
               box: {strokeWidth: 0},
               init() {
                  let ret = {}
                  let n = this.getIndex("number") + ""
                  ret.num = new fabric.Text(n, {
                     fontSize: {{timeline.font_size}},
                     originX: "center",
                     originY: "center",
                     fontFamily: "monospace",
                  })
                  return ret
               },
               where: {left: {{(timeline.slot_width-timeline.font_size)/2}}, top: {{(timeline.header_height - timeline.font_size)/2}}},
               layout: {left: {{timeline.spacing}}}
