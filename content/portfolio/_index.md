+++
title = "Portfolio"
description = "A selection of my favourite side projects"

[extra]
photo = "lakeside"
+++

## Cloudbase

Cloudbase is a flight instrument for paragliders that runs on your phone. It shows your speed,
altitude and climb/sink rate, estimates the wind from how you drift while circling, and marks where you
found lift on the map so you can get back to it. It also displays horizontal and vertical airspace
limits and warns as you approach a boundary. It's small, simple and is designed to run lightly on
low-spec hardware.

{{ <gallery app="cloudbase" shots={[
  "1-thermalling | Cloudbase map showing a paraglider circling in a thermal, with speed, altitude, climb rate and wind across the top",
  "2-airspace-alert | Cloudbase warning that the pilot is inside Queenstown controlled airspace",
  "3-between-thermals | Cloudbase map showing the track between two thermals, with a side view of the terrain ahead",
  "4-on-glide | Cloudbase map showing a glide across a valley, with the airspace boundary ahead",
  "5-settings | Cloudbase settings for the glider and airspace alerts",
]} /> }}

## Needle

Needle is a car diagnostics app. It connects to a Bluetooth OBD2 adapter and shows what the car
knows about itself: how much fuel is left and how far that will get you, live readings from the
engine's sensors, and any fault codes.

{{ <gallery app="needle" shots={[
  "1-fuel-gauge | Needle fuel gauge showing 58% full, 391 km of range and current fuel use",
  "2-live-sensors | Needle showing live readings from eight engine sensors, each with a small graph",
  "3-sensor-detail | Needle showing engine speed on a dial with a graph of recent readings",
  "4-trouble-codes | Needle listing the fault codes behind a check engine light, with a description of each",
  "5-emissions-readiness | Needle showing which of the car's emissions self-tests have finished",
]} /> }}
