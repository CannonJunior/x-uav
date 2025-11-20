# Visual Requirements for UAV Comparison Application

## Overview
This document outlines the visual asset requirements for the X-UAV comparison web application. Three types of visual assets are required for each UAV to provide comprehensive visual comparison capabilities.

## 1. Accurate Imagery

### Purpose
Provide high-quality photographic or rendered images of each UAV for identification and general viewing.

### Requirements
- **Format**: PNG or JPEG
- **Resolution**: Minimum 1920x1080 pixels
- **Aspect Ratio**: 16:9 or original aspect ratio
- **Views Required**:
  - Primary: Side profile view (preferred)
  - Secondary: Three-quarter view showing both side and front/rear
  - Optional: Additional views (front, rear, top, bottom)
- **Background**: Transparent PNG preferred, or clean neutral background
- **Quality**: High resolution, professional quality
- **Accuracy**: Must accurately represent the actual UAV design
- **Storage Path**: `/frontend/public/assets/images/uavs/{designation}/`
- **Naming Convention**: `{designation}-{view}.png` (e.g., `mq-9-side.png`)

### Data Integration
- Store primary image URL in database: `imagery_url` field
- Support multiple image URLs for different views: `imagery_urls` JSON array

### Sources
- Official manufacturer press kits
- Defense department public affairs imagery
- Open-source intelligence (OSINT) photography
- Accurate 3D renders from reputable sources
- Wikipedia Commons (with proper licensing)

---

## 2. Overhead Silhouettes

### Purpose
Provide accurately scaled overhead (top-down) silhouettes for size comparison visualization.

### Requirements
- **Format**: SVG (Scalable Vector Graphics) preferred for infinite scaling
- **Fallback Format**: PNG with transparent background at 2000x2000 pixels minimum
- **View**: Directly overhead (top-down) view
- **Color**: Solid black silhouette or single color fill
- **Background**: Transparent
- **Accuracy**: Must accurately depict:
  - Wingspan (most critical dimension)
  - Overall length
  - Wingtip shape
  - Fuselage shape
  - Tail configuration (if applicable)
  - Sensor pods or external fixtures
- **Scale**: All silhouettes must be in the same scale relative to actual dimensions
  - Use wingspan as primary scaling reference
  - Store scale metadata: pixels per meter ratio
- **Storage Path**: `/frontend/public/assets/silhouettes/{designation}/`
- **Naming Convention**: `{designation}-overhead.svg` or `{designation}-overhead.png`

### Scaling System
- **Reference Scale**: 1 meter = 100 pixels (configurable)
- **Scale Factor Storage**: Store in database `scale_factor` field
- **Calculation**: `image_width_pixels = wingspan_meters * 100`
- **Example**: MQ-9 Reaper with 20.1m wingspan = 2010 pixels width

### Comparison Display
- Overlay multiple silhouettes on a grid for visual size comparison
- Display actual dimensions alongside silhouettes
- Allow zoom and pan for detailed inspection
- Show scale reference (e.g., "50m" scale bar)

### Creation Methods
- Trace from accurate overhead photographs
- Extract from official technical drawings
- Generate from 3D models (top orthographic view)
- Manual creation based on documented dimensions

---

## 3. 3D Models

### Purpose
Provide interactive 3D models that can be rotated and viewed from any angle for detailed examination.

### Requirements
- **Format**: glTF 2.0 (.gltf or .glb) - industry standard for web 3D
- **Alternative Formats**: OBJ, FBX (will require conversion)
- **Polygon Count**:
  - Low-poly version: 5,000-20,000 triangles (for web performance)
  - High-poly version: 50,000-200,000 triangles (for detailed inspection)
- **Textures**:
  - PBR (Physically Based Rendering) materials preferred
  - Diffuse, normal, roughness, metallic maps
  - Texture resolution: 2048x2048 or 4096x4096
- **Scale**: Accurate real-world scale (meters)
- **Pivot Point**: Centered at center of gravity or geometric center
- **Storage Path**: `/frontend/public/assets/models/{designation}/`
- **Naming Convention**:
  - Low-poly: `{designation}-low.glb`
  - High-poly: `{designation}-high.glb`

### Model Requirements
- **Accuracy**: Must accurately represent:
  - Overall dimensions (length, wingspan, height)
  - Fuselage shape
  - Wing configuration
  - Landing gear (retracted and deployed states optional)
  - Sensor turrets and pods
  - Weapons hardpoints (if UCAV)
- **UV Mapping**: Proper UV unwrapping for textures
- **Materials**: PBR materials for realistic rendering
- **Optimization**: Optimized for web rendering (minimal draw calls)

### Interactive Features
- **Rotation**: Full 360° rotation on all axes
- **Zoom**: Smooth zoom in/out
- **Pan**: Pan/translate model view
- **Preset Views**: Buttons for standard views (front, side, top, 3/4)
- **Animation** (optional):
  - Rotating propeller/rotor
  - Landing gear deployment
  - Weapons bay opening (if applicable)
- **Annotations** (optional): Clickable hotspots for component information

### 3D Viewer Technology
- **Library**: Three.js (WebGL-based 3D library)
- **File Loader**: GLTFLoader for .gltf/.glb files
- **Controls**: OrbitControls for camera manipulation
- **Lighting**:
  - Ambient light for base illumination
  - Directional light for shadows and depth
  - Environment map for reflections (optional)
- **Performance**:
  - LOD (Level of Detail) system for large models
  - Lazy loading - load model only when viewed
  - Progressive loading for large files

### Sources
- Free 3D model repositories (Sketchfab, TurboSquid Free section)
- Government/defense contractor press kits
- Open-source 3D modeling community
- Custom modeling based on technical drawings
- Photogrammetry from multiple images

---

## Asset Storage Structure

```
frontend/public/assets/
├── images/
│   └── uavs/
│       ├── mq-9/
│       │   ├── mq-9-side.png
│       │   ├── mq-9-front.png
│       │   └── mq-9-three-quarter.png
│       ├── rq-4/
│       └── tb2/
├── silhouettes/
│   ├── mq-9-overhead.svg
│   ├── rq-4-overhead.svg
│   └── tb2-overhead.svg
└── models/
    ├── mq-9/
    │   ├── mq-9-low.glb
    │   ├── mq-9-high.glb
    │   └── textures/
    ├── rq-4/
    └── tb2/
```

---

## Database Schema Integration

Each UAV record should include:
```json
{
  "designation": "MQ-9",
  "imagery_urls": {
    "side": "/assets/images/uavs/mq-9/mq-9-side.png",
    "front": "/assets/images/uavs/mq-9/mq-9-front.png",
    "three_quarter": "/assets/images/uavs/mq-9/mq-9-three-quarter.png"
  },
  "silhouette_url": "/assets/silhouettes/mq-9-overhead.svg",
  "model_urls": {
    "low_poly": "/assets/models/mq-9/mq-9-low.glb",
    "high_poly": "/assets/models/mq-9/mq-9-high.glb"
  },
  "scale_factor": 100
}
```

---

## Implementation Phases

### Phase 1: Table Display with Images (Current)
- Implement basic table with UAV specifications
- Add primary side-view imagery for each UAV
- Focus: Data display and comparison

### Phase 2: Silhouette Comparison View
- Create scaled overhead silhouettes for all UAVs
- Implement silhouette comparison overlay feature
- Add interactive size comparison tool
- Focus: Visual size comparison

### Phase 3: 3D Model Viewer
- Integrate Three.js 3D viewer
- Add 3D models for UAVs
- Implement interactive controls
- Add preset camera positions
- Focus: Detailed 3D inspection

### Phase 4: Enhanced Visualization
- Add multiple views in image gallery
- Implement model animations
- Add component annotations
- Create comparison mode for 3D models
- Focus: Advanced visual features

---

## Asset Acquisition Strategy

### Immediate (Phase 1)
1. Search for Creative Commons licensed images
2. Use official government/manufacturer press images
3. Screenshot from public videos (with attribution)
4. Generate placeholders for missing assets

### Short-term (Phase 2)
1. Create accurate silhouettes from available imagery
2. Commission custom silhouettes if needed
3. Ensure all silhouettes are properly scaled

### Long-term (Phase 3)
1. Search for free 3D models on Sketchfab, Free3D, etc.
2. Commission custom 3D models for key UAVs
3. Leverage open-source modeling community
4. Create simplified models from technical drawings

---

## Legal & Licensing Considerations

- **Public Domain**: Prioritize US government/military imagery (public domain)
- **Creative Commons**: Use CC-licensed imagery with proper attribution
- **Fair Use**: Educational and comparison purposes may qualify
- **Manufacturer Permission**: Request permission for official imagery
- **ITAR Compliance**: Ensure no classified or export-controlled information
- **Attribution**: Properly credit all image sources
- **Licensing File**: Maintain `LICENSES.md` with all asset attributions

---

## Quality Assurance

### Image QA Checklist
- [ ] Resolution meets minimum requirements
- [ ] Accurate representation of UAV
- [ ] Clean background or transparent
- [ ] Proper aspect ratio
- [ ] No watermarks or artifacts
- [ ] Correct file naming convention

### Silhouette QA Checklist
- [ ] Accurate overhead perspective
- [ ] Correct wingspan-to-length ratio
- [ ] Properly scaled relative to other UAVs
- [ ] Clean vector paths (if SVG)
- [ ] Transparent background
- [ ] No distortion or skewing

### 3D Model QA Checklist
- [ ] Accurate dimensions in real-world scale
- [ ] Optimized polygon count
- [ ] Proper UV mapping
- [ ] Textures load correctly
- [ ] Model centered at origin
- [ ] No rendering artifacts
- [ ] Smooth rotation/zoom performance
- [ ] File size reasonable for web (<10MB for low-poly)

---

## Future Enhancements

- **AR/VR Support**: WebXR integration for immersive viewing
- **Comparison Mode**: Side-by-side 3D model comparison
- **Animation**: Flight dynamics simulation
- **Environmental Context**: Display models in operational environments
- **Scale References**: Add human figures or vehicles for scale
- **Component Breakdown**: Exploded view of UAV components
- **Historical Timeline**: Show evolution of UAV designs over time
