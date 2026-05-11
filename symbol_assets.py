# connectivity stuff
pin = '''(pin {electrical_type} {graphic_style}
  (at {x} {y} {orientation})
  (length {length})
  (name "{name}"
    (effects
      (font
        (size {name_size_x} {name_size_y}))))
  (number "{number}"
    (effects
      (font
        (size {number_size_x} {number_size_y})))))'''

# shapes
rectangle = '''(rectangle
  (start {start_x} {start_y})
  (end {end_x} {end_y})
  (stroke
    (width {stroke_width})
    (type {stroke_type}))
  (fill
    (type {fill_type})))'''

#text box
text_box = '''(text "{text_content}"
  (at {x} {y} {orientation})
  (effects
    (font
      (size {font_size_x} {font_size_y}))))'''