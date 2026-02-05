import pygame
import sys
try:
    import moderngl
    import struct
except ImportError:
    moderngl = None

class ShaderRenderer:
    def __init__(self, width, height):
        if not moderngl:
            print("WARNING: moderngl not installed. GPU effects disabled.")
            self.ctx = None
            return

        self.ctx = moderngl.create_context()
        self.ctx.enable(moderngl.BLEND)
        
        # Quad (Full screen triangle strip)
        # x, y, u, v
        self.quad_buffer = self.ctx.buffer(struct.pack('16f', 
            -1.0, 1.0, 0.0, 0.0,  # Top Left
            -1.0, -1.0, 0.0, 1.0, # Bottom Left
             1.0, 1.0, 1.0, 0.0,  # Top Right
             1.0, -1.0, 1.0, 1.0  # Bottom Right
        ))
        
        self.program = self.ctx.program(
            vertex_shader='''
                #version 330
                in vec2 vert;
                in vec2 texcoord;
                out vec2 v_text;
                void main() {
                    gl_Position = vec4(vert, 0.0, 1.0);
                    v_text = texcoord;
                }
            ''',
            fragment_shader='''
                #version 330
                uniform sampler2D tex;
                in vec2 v_text;
                out vec4 f_color;

                void main() {
                    vec2 uv = v_text;
                    
                    // --- Tilt Shift Blur (Vertical only for speed) ---
                    float v_blur = smoothstep(0.25, 0.0, uv.y) + smoothstep(0.75, 1.0, uv.y);
                    
                    vec4 color_source = texture(tex, uv);
                    
                    if (v_blur > 0.01) {
                        float blur_size = 0.005 * v_blur; 
                        vec4 sum = vec4(0.0);
                        float total_w = 0.0;
                        
                        // 9-sample blur
                        for(float x = -1.0; x <= 1.0; x += 1.0) {
                            for(float y = -1.0; y <= 1.0; y += 1.0) {
                                float weight = 1.0 - abs(x) * 0.5; // simple weight
                                vec4 s = texture(tex, uv + vec2(x * blur_size, y * blur_size));
                                sum += s * weight;
                                total_w += weight;
                            }
                        }
                        color_source = sum / total_w;
                    }

                    // --- Vignette ---
                    vec2 center = uv - 0.5;
                    float dist = length(center);
                    // Lighter vignette:
                    // Reduced multiplier to 1.1 (pushes effect to corners)
                    // Scaled smoothstep output by 0.6 so it only darkens by 60% max, not 100%
                    float vign_val = smoothstep(0.4, 0.9, dist * 1.1);
                    float vign = 1.0 - (vign_val * 0.6); 
                    
                    // Apply
                    color_source.rgb *= vign;
                    
                    // FORCE ALPHA TO 1.0
                    // Pygame surfaces often have undefined alpha in non-per-pixel mode,
                    // which can result in transparent black if blending is on.
                    f_color = vec4(color_source.rgb, 1.0);
                }
            '''
        )
        
        self.vao = self.ctx.vertex_array(self.program, [
            (self.quad_buffer, '2f 2f', 'vert', 'texcoord')
        ])
        
        # Texture
        # Pygame surfaces are usually 32-bit (RGBA) by default, so we use 4 components
        self.texture = self.ctx.texture((width, height), 4)
        self.texture.filter = (moderngl.LINEAR, moderngl.LINEAR)
        
        # Pygame uses BGRA usually on little-endian systems (Windows/Linux x86)
        # We try to swizzle. If colors look weird (blue skin), we can remove this or swap.
        # But usually 'BGRA' is safer for Pygame -> OpenGL
        self.texture.swizzle = 'BGRA'

    def render(self, surface):
        if not self.ctx:
            # Fallback if no shader support
            display = pygame.display.get_surface()
            display.blit(surface, (0,0))
            return

        # Convert surface to texture
        # Using get_view('3') can return non-contiguous memory which moderngl dislikes.
        # We must convert it to bytes directly.
        
        # Method 1: Pygame image to string (slow but safe)
        # raw_data = pygame.image.tostring(surface, 'RGB')
        
        # Method 2: Get View and bytes() (faster)
        # We need to flip it because OpenGL UVs are often inverted relative to Pygame
        # But our shader handles UVs standardly. Let's see.
        
        # Fix for "BufferError: A 3D surface view is not contiguous"
        # We need to ensure the data is contiguous.
        
        # The fastest way in Pygame 2 to get bytes for ModernGL:
        raw_data = surface.get_view('1') # Get flat view
        self.texture.write(raw_data)
        self.texture.use()
        
        # Render
        self.ctx.clear(0.0, 0.0, 0.0)
        self.vao.render(moderngl.TRIANGLE_STRIP)
