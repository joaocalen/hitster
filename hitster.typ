#let songs = json("songs.json")

//this is a4
#let page_width = 210mm
#let page_height = 297mm

#let margin_x = 1cm
#let margin_y = 0.5cm

#let rows = 5
#let cols = 3
#let card_size = 5cm

#let marking_padding = 1cm

// Approx check (gutter is small but matters, margins are double)
#assert(rows * card_size + 2 * marking_padding + 2 * margin_y <= page_height)
#assert(cols * card_size + 2 * marking_padding + 2 * margin_x <= page_width)

#set page(
  width: page_width,
  height: page_height,
  margin: (
    x: margin_x,
    y: margin_y
  )
)

#set text(font: "New Computer Modern")

#let card_bg_color = luma(240)
#let card_stroke = 2pt + black

#let qr_front_side(song) = {
  box(
    width: card_size,
    height: card_size,
    fill: card_bg_color,
    stroke: card_stroke,
    inset: 0.5cm,
    radius: 4mm,
    align(center + horizon)[
      #image(
        "qr_codes/" + song.id + ".svg",
        width: 100%
      )
    ]
  )
}

#let text_back_side(song) = {
  box(
    width: card_size,
    height: card_size,
    fill: card_bg_color,
    stroke: card_stroke,
    radius: 4mm,
    inset: 0.2cm,
    stack(
      spacing: 5pt,
      dir: ttb,
      
      // Artist
      block(
        width: 100%,
        height: 25%,
        align(center + horizon)[
          #text(
            song.artists.map(artist => artist).join(", "),
            size: 11pt,
            weight: "bold",
            font: "Roboto"
          )
        ]
      ),
      
      // Song Name
      block(
        width: 100%,
        height: 35%,
        align(center + horizon)[
          #text(
            song.name,
            size: 13pt,
            style: "italic",
            font: "Roboto"
          )
        ]
      ),

      // Year (Big)
      block(
        width: 100%,
        height: 30%,
        align(center + horizon)[
          #text(
            str(song.year),
            size: 28pt,
            weight: "black",
            fill: rgb("#d32f2f"), // A distinct color for the year
            font: "Roboto"
          )
        ]
      )
    )
  )
}

#let marking_line = line(
  stroke: (
    paint: gray,
    thickness: 0.5pt
  ),
  length: marking_padding / 2
)

//a rotatable box with cut markings
#let marking(angle) = {
  rotate(
    angle,
    reflow: true,
    box(
      width: marking_padding,
      height: card_size,
      stack(
        spacing: card_size,
        ..(marking_line,) * 2
      )
    )
  )
}

//a row of markings
#let marking_row(angle) = {
  (
    square(
      size: marking_padding,
    ),
    ..(marking(angle),) * cols,
    square(
      size: marking_padding,
    ),
  )
}

#let pad_page(page) = {
  let rows = page.chunks(cols)

  //pad left and right
  let padded_rows = rows.map(
    row => (
      marking(0deg),
      row,
      marking(180deg)
    )
  )

  //pad top and bottom
  return (
    ..marking_row(90deg),
    ..padded_rows.flatten(),
    ..marking_row(270deg)
  )
}


#let get_pages(songs) = {
  let pages = ()

  //add test and qr codes
  for page in songs.chunks(rows*cols) {
    let fronts = ()
    let backs = ()

    for song in page {
      fronts.push(qr_front_side(song))
      backs.push(text_back_side(song))
    }

    //fill remaining slots with empty boxes if needed
    for _ in range(rows * cols - page.len()) {
      fronts.push(
        square(
          size: card_size
        )
      )
      backs.push(
        square(
          size: card_size
        )
      )
    }

    //reverse back side
    let back_rows = backs.chunks(cols)
    let reversed_back_rows = back_rows.map(row => row.rev())
    let reversed_backs = reversed_back_rows.flatten()

    pages.push(pad_page(fronts))
    pages.push(pad_page(reversed_backs))
  }
  return pages
}

#for (i, page) in get_pages(songs).enumerate() {
  if i != 0 {
    pagebreak()
  }
  grid(
    columns: cols + 2,
    gutter: 2mm, // Add gutter spacing
    ..page
  )
}
