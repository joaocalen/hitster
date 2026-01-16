#set page(
  paper: "a4",
  margin: 1cm,
)

#let token_size = 40mm
#let token_count = 37

#let cols = 4
#let rows = 6

#let token() = {
  box(
    width: token_size,
    height: token_size,
    {
      // 1. Vinyl Base (Black)
      circle(
        radius: token_size / 2,
        fill: black,
        stroke: none
      )
      
      // 2. Grooves (Subtle gray rings)
      place(center + horizon, circle(radius: token_size * 0.45, stroke: (thickness: 0.5pt, paint: luma(60)), fill: none))
      place(center + horizon, circle(radius: token_size * 0.40, stroke: (thickness: 0.5pt, paint: luma(60)), fill: none))
      place(center + horizon, circle(radius: token_size * 0.35, stroke: (thickness: 0.5pt, paint: luma(60)), fill: none))
      
      // 3. Label (Red)
      place(center + horizon, 
        circle(
          radius: token_size * 0.25,
          fill: rgb("#d32f2f"),
          stroke: none
        )
      )
      
      // 4. Icon (Music Note)
      place(center + horizon,
        text(size: 18pt, fill: white, font: "New Computer Modern")[♫]
      )
      
    }
  )
}

#let tokens = ()
#for i in range(token_count) {
  tokens.push(token())
}

#let chunks = tokens.chunks(rows * cols)

#for (i, chunk) in chunks.enumerate() {
  if i > 0 {
    pagebreak()
  }
  grid(
    columns: cols,
    gutter: 5mm,
    ..chunk
  )
}
