## The Dry Side to Wet Side wiring connection is described as such:

    WHITE common
       ├── Valve 1 lead
       ├── Valve 2 lead
       ├── Valve 3 lead
       └── Valve 4 lead

    RED    -> Valve 1 other lead
    GREEN  -> Valve 2 other lead
    BLACK  -> Valve 3 other lead
    YELLOW -> Valve 4 other lead

## Next Version

- Put the 10 minute timer default in the ESP32 code. Also - at the same time
  change the 10 Min button to a '+10 Min' button.  A press when a zone off sets
  timer for 10 min.  A subsequent press while the zone is on adds 10 Min (changing the off time).
  Multiple +10 presses are allowed,  and the OFF press turns the zone off immediately
  and cancels any future planned OFF. 
- Build in Flow Sensor
- Make dry side smaller and waterproof.
-
