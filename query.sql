-- insert catergory
INSERT INTO `musikita_db`.`product_category`
(`categoryName`)
VALUES
("Acoustic"),
("Electric"),
("Percussion"),
("Keys & Midi"),
("Recording Kit"),
("Sound System"),
("Accessories"),
("DAW & Plugins");

-- insert subcategory
INSERT INTO `musikita_db`.`product_subcategory`
(`categoryId_id`, `subCategoryName`)
VALUES
(1, "Guitar"),
(1, "Bass"),
(1, "Orchestra Instruments"),
(2, "Guitar"),
(2, "Bass"),
(2, "Orchestra Instruments"),
(3, "Electric drums"),
(3, "Tom"),
(3, "Cymbal"),
(3, "Hat"),
(3, "Snare"),
(3, "Bass Drum"),
(4, "Piano"),
(4, "Keyboard"),
(4, "MIDI Keyboard"),
(4, "Synthesizer"),
(5, "Microphone"),
(5, "Audio Interface"),
(5, "Monitor Speaker"),
(5, "Headphone"),
(6, "Speaker"),
(6, "Mixer"),
(6, "Amplifier"),
(6, "Processor"),
(7, "String"),
(7, "Tuner"),
(7, "Pick"),
(7, "Capo"),
(7, "Other"),
(8, "Daw Software"),
(8, "Plugins");