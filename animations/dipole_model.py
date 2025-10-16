"""
Manim animation illustrating the dipole model in EEG neurophysiology.

This animation demonstrates:
1. A pyramidal neuron with apical dendrites and soma
2. An EPSP arriving at the dendrites (Na+ influx)
3. Formation of current sink (negative extracellular) at dendrites
4. Formation of current source (positive extracellular) at soma
5. The resulting dipole and electric field lines
"""

from manim import *


class DipoleModel(Scene):
    def construct(self):
        # Title - using Tex for better rendering
        title = Tex(r"\textbf{The Dipole Model}", font_size=48)
        subtitle = Tex(
            r"How synaptic activity creates measurable electric fields", font_size=24, color=GRAY
        )
        subtitle.next_to(title, DOWN)

        self.play(FadeIn(title, shift=UP * 0.3))
        self.play(FadeIn(subtitle, shift=UP * 0.2))
        self.wait(1)
        self.play(FadeOut(title), FadeOut(subtitle))

        # Draw a simplified pyramidal neuron
        self.show_neuron_structure()

        # Show EPSP arriving at dendrites
        self.show_epsp_arrival()

        # Show ion flow and dipole formation
        self.show_dipole_formation()

        # Show electric field propagation
        self.show_electric_field()

    def show_neuron_structure(self):
        """Draw a simplified pyramidal neuron."""
        # Soma (cell body) - circle at bottom
        soma = Circle(radius=0.3, color=BLUE, fill_opacity=0.3)
        soma.shift(DOWN * 1.5)

        # Axon extending down from soma
        axon = Line(soma.get_bottom(), soma.get_bottom() + DOWN * 0.8, color=BLUE, stroke_width=3)

        # Apical dendrite - main trunk going up
        dendrite_trunk = Line(soma.get_top(), soma.get_top() + UP * 2.5, color=BLUE, stroke_width=4)

        # Branching dendrites at top
        dendrite_top = dendrite_trunk.get_end()
        dendrite_branch1 = Line(
            dendrite_top, dendrite_top + UP * 0.5 + LEFT * 0.4, color=BLUE, stroke_width=3
        )
        dendrite_branch2 = Line(
            dendrite_top, dendrite_top + UP * 0.5 + RIGHT * 0.4, color=BLUE, stroke_width=3
        )

        # Small branches
        branch1_end = dendrite_branch1.get_end()
        dendrite_branch1a = Line(
            branch1_end, branch1_end + UP * 0.3 + LEFT * 0.2, color=BLUE, stroke_width=2
        )
        dendrite_branch1b = Line(
            branch1_end, branch1_end + UP * 0.3 + RIGHT * 0.1, color=BLUE, stroke_width=2
        )

        branch2_end = dendrite_branch2.get_end()
        dendrite_branch2a = Line(
            branch2_end, branch2_end + UP * 0.3 + RIGHT * 0.2, color=BLUE, stroke_width=2
        )
        dendrite_branch2b = Line(
            branch2_end, branch2_end + UP * 0.3 + LEFT * 0.1, color=BLUE, stroke_width=2
        )

        # Group all neuron parts
        self.neuron = VGroup(
            soma,
            axon,
            dendrite_trunk,
            dendrite_branch1,
            dendrite_branch2,
            dendrite_branch1a,
            dendrite_branch1b,
            dendrite_branch2a,
            dendrite_branch2b,
        )

        # Labels
        soma_label = Tex(r"Soma", font_size=20).next_to(soma, RIGHT, buff=0.3)
        dendrite_label = Tex(r"Apical Dendrites", font_size=20).next_to(
            dendrite_top, RIGHT, buff=0.3
        )

        self.play(Create(self.neuron), run_time=2)
        self.play(FadeIn(soma_label), FadeIn(dendrite_label))
        self.wait(1)
        self.play(FadeOut(soma_label), FadeOut(dendrite_label))

        # Store key positions
        self.soma_center = soma.get_center()
        self.dendrite_top_pos = dendrite_top

    def show_epsp_arrival(self):
        """Show an EPSP arriving at the dendrites."""
        # Label for EPSP
        epsp_label = Tex(r"EPSP arrives", font_size=24, color=YELLOW)
        epsp_label.to_edge(UP)

        self.play(FadeIn(epsp_label))

        # Show synapse with neurotransmitter release
        synapse_pos = self.dendrite_top_pos + LEFT * 0.6 + UP * 0.2

        # Presynaptic terminal
        presynaptic = Circle(radius=0.15, color=YELLOW, fill_opacity=0.5)
        presynaptic.move_to(synapse_pos + LEFT * 0.3)

        # Neurotransmitter vesicles
        vesicles = VGroup(
            *[
                Dot(radius=0.03, color=ORANGE).move_to(
                    presynaptic.get_center()
                    + np.array([np.random.uniform(-0.1, 0.1), np.random.uniform(-0.1, 0.1), 0])
                )
                for _ in range(8)
            ]
        )

        self.play(FadeIn(presynaptic), FadeIn(vesicles))

        # Show vesicle release and Na+ ions entering
        postsynaptic_pos = synapse_pos + RIGHT * 0.3

        # Na+ ions
        na_ions = VGroup(
            *[
                VGroup(
                    Circle(radius=0.05, color=RED, fill_opacity=0.8),
                    MathTex("+", font_size=12, color=WHITE).move_to(ORIGIN),
                ).move_to(presynaptic.get_center() + RIGHT * 0.1 * i)
                for i in range(5)
            ]
        )

        self.play(
            *[vesicle.animate.move_to(postsynaptic_pos) for vesicle in vesicles[:4]], run_time=0.5
        )

        self.play(
            FadeIn(na_ions),
            *[ion.animate.shift(RIGHT * 0.5 + DOWN * 0.3) for ion in na_ions],
            run_time=1,
        )

        self.wait(0.5)
        self.play(FadeOut(epsp_label), FadeOut(presynaptic), FadeOut(vesicles), FadeOut(na_ions))

    def show_dipole_formation(self):
        """Show the formation of current sink and source."""
        # Explanatory text
        sink_text = Tex(r"Current Sink $(-)$", font_size=24, color=BLUE)
        sink_text.to_edge(UP).shift(LEFT * 3)

        source_text = Tex(r"Current Source $(+)$", font_size=24, color=RED)
        source_text.to_edge(UP).shift(RIGHT * 3)

        self.play(FadeIn(sink_text), FadeIn(source_text))

        # Negative charge accumulation at dendrites (extracellular)
        sink_region = Circle(radius=0.6, color=BLUE, fill_opacity=0.2, stroke_width=2).move_to(
            self.dendrite_top_pos
        )

        minus_signs = VGroup(
            *[
                MathTex("-", font_size=30, color=BLUE).move_to(
                    sink_region.get_center()
                    + np.array([np.cos(i * TAU / 6), np.sin(i * TAU / 6), 0]) * 0.4
                )
                for i in range(6)
            ]
        )

        # Positive charge accumulation at soma (extracellular)
        source_region = Circle(radius=0.5, color=RED, fill_opacity=0.2, stroke_width=2).move_to(
            self.soma_center
        )

        plus_signs = VGroup(
            *[
                MathTex("+", font_size=30, color=RED).move_to(
                    source_region.get_center()
                    + np.array([np.cos(i * TAU / 6), np.sin(i * TAU / 6), 0]) * 0.35
                )
                for i in range(6)
            ]
        )

        self.play(
            FadeIn(sink_region), FadeIn(minus_signs), FadeIn(source_region), FadeIn(plus_signs)
        )

        # Show dipole arrow
        dipole_arrow = Arrow(
            self.soma_center, self.dendrite_top_pos, color=PURPLE, stroke_width=6, buff=0.5
        )

        dipole_label = Tex(r"Dipole", font_size=24, color=PURPLE)
        dipole_label.next_to(dipole_arrow, RIGHT, buff=0.3)

        self.wait(1)
        self.play(GrowArrow(dipole_arrow), FadeIn(dipole_label))
        self.wait(2)

        # Store for next scene
        self.sink_region = sink_region
        self.source_region = source_region
        self.minus_signs = minus_signs
        self.plus_signs = plus_signs
        self.dipole_arrow = dipole_arrow

        self.play(FadeOut(sink_text), FadeOut(source_text), FadeOut(dipole_label))

    def show_electric_field(self):
        """Show the electric field lines radiating from the dipole."""
        field_label = Tex(r"Electric field propagates through tissue", font_size=28, color=YELLOW)
        field_label.to_edge(UP)

        self.play(FadeIn(field_label))

        # Create field lines emanating from the dipole
        field_lines = VGroup()

        # Lines going from positive (soma) to negative (dendrites)
        num_lines = 12
        for i in range(num_lines):
            angle = i * TAU / num_lines

            # Start from source region (soma)
            start = (
                self.source_region.get_center() + np.array([np.cos(angle), np.sin(angle), 0]) * 0.5
            )

            # Curve to sink region (dendrites)
            # Use a bezier curve for realistic field lines
            control1 = start + np.array([np.cos(angle), np.sin(angle), 0]) * 1.5
            control2 = (
                self.sink_region.get_center()
                + np.array([np.cos(angle + PI), np.sin(angle + PI), 0]) * 1.0
            )
            end = (
                self.sink_region.get_center()
                + np.array([np.cos(angle + PI), np.sin(angle + PI), 0]) * 0.6
            )

            # Create curved path
            path = CubicBezier(start, control1, control2, end)
            field_line = path.set_color(GREEN).set_stroke(width=2, opacity=0.6)

            # Add arrowhead
            arrow_tip = (
                ArrowTriangleFilledTip(color=GREEN, fill_opacity=0.8)
                .scale(0.15)
                .move_to(end)
                .rotate(np.arctan2((end - control2)[1], (end - control2)[0]) + PI / 2)
            )

            field_lines.add(VGroup(field_line, arrow_tip))

        self.play(Create(field_lines), run_time=3)

        # Add explanation
        explanation = Tex(
            r"This field reaches the scalp where we can measure it with EEG!",
            font_size=24,
            color=WHITE,
        ).to_edge(DOWN)

        self.play(FadeIn(explanation))
        self.wait(2)

        # Store the current scene state for summary
        self.field_lines = field_lines
        self.field_label = field_label
        self.explanation = explanation

        # Show summary timeline
        self.show_summary_timeline()

    def show_summary_timeline(self):
        """Create a summary showing key steps in sequence."""
        # Fade out ALL current scene elements
        self.play(
            FadeOut(self.neuron),
            FadeOut(self.sink_region),
            FadeOut(self.minus_signs),
            FadeOut(self.source_region),
            FadeOut(self.plus_signs),
            FadeOut(self.dipole_arrow),
            FadeOut(self.field_lines),
            FadeOut(self.field_label),
            FadeOut(self.explanation),
            run_time=0.8,
        )

        # Create title
        summary_title = Tex(r"\textbf{The Dipole Formation Process}", font_size=36)
        summary_title.to_edge(UP)
        self.play(FadeIn(summary_title))

        # Create 4 snapshot panels showing key stages
        panel_width = 2.8
        panel_spacing = 0.3
        start_x = -5.5

        # Step 1: Neuron structure
        step1 = self.create_snapshot_neuron()
        step1.scale(0.35).move_to([start_x + panel_width / 2, 0.3, 0])
        step1_label = Tex(r"1. Pyramidal \\ Neuron", font_size=16).next_to(step1, DOWN, buff=0.2)

        # Step 2: EPSP arrival
        step2 = self.create_snapshot_epsp()
        step2.scale(0.35).move_to([start_x + panel_width + panel_spacing + panel_width / 2, 0.3, 0])
        step2_label = Tex(r"2. EPSP \\ Arrival", font_size=16).next_to(step2, DOWN, buff=0.2)

        # Step 3: Dipole formation
        step3 = self.create_snapshot_dipole()
        step3.scale(0.35).move_to(
            [start_x + 2 * (panel_width + panel_spacing) + panel_width / 2, 0.3, 0]
        )
        step3_label = Tex(r"3. Dipole \\ Formation", font_size=16).next_to(step3, DOWN, buff=0.2)

        # Step 4: Electric field
        step4 = self.create_snapshot_field()
        step4.scale(0.35).move_to(
            [start_x + 3 * (panel_width + panel_spacing) + panel_width / 2, 0.3, 0]
        )
        step4_label = Tex(r"4. Electric \\ Field", font_size=16).next_to(step4, DOWN, buff=0.2)

        # Animate panels appearing in sequence
        self.play(FadeIn(step1), FadeIn(step1_label), run_time=0.8)
        self.play(FadeIn(step2), FadeIn(step2_label), run_time=0.8)
        self.play(FadeIn(step3), FadeIn(step3_label), run_time=0.8)
        self.play(FadeIn(step4), FadeIn(step4_label), run_time=0.8)

        self.wait(3)

    def create_snapshot_neuron(self):
        """Create a small version of just the neuron."""
        soma = Circle(radius=0.3, color=BLUE, fill_opacity=0.3)
        soma.shift(DOWN * 1.5)

        axon = Line(soma.get_bottom(), soma.get_bottom() + DOWN * 0.8, color=BLUE, stroke_width=3)

        dendrite_trunk = Line(soma.get_top(), soma.get_top() + UP * 2.5, color=BLUE, stroke_width=4)

        dendrite_top = dendrite_trunk.get_end()
        dendrite_branch1 = Line(
            dendrite_top, dendrite_top + UP * 0.5 + LEFT * 0.4, color=BLUE, stroke_width=3
        )
        dendrite_branch2 = Line(
            dendrite_top, dendrite_top + UP * 0.5 + RIGHT * 0.4, color=BLUE, stroke_width=3
        )

        return VGroup(soma, axon, dendrite_trunk, dendrite_branch1, dendrite_branch2)

    def create_snapshot_epsp(self):
        """Create snapshot with EPSP indication."""
        neuron = self.create_snapshot_neuron()

        # Add synapse indicator at top
        synapse = Circle(radius=0.2, color=YELLOW, fill_opacity=0.7)
        synapse.move_to(neuron[2].get_end() + UP * 0.5 + LEFT * 0.5)

        # Add Na+ ions
        na_ion = VGroup(
            Circle(radius=0.08, color=RED, fill_opacity=0.8),
            MathTex("+", font_size=14, color=WHITE),
        )
        na_ion.move_to(synapse.get_center() + RIGHT * 0.3)

        return VGroup(neuron, synapse, na_ion)

    def create_snapshot_dipole(self):
        """Create snapshot showing dipole formation."""
        neuron = self.create_snapshot_neuron()
        soma_center = neuron[0].get_center()
        dendrite_top = neuron[2].get_end()

        # Sink at dendrites
        sink = Circle(radius=0.6, color=BLUE, fill_opacity=0.2, stroke_width=2)
        sink.move_to(dendrite_top)
        minus_signs = VGroup(
            *[
                MathTex("-", font_size=20, color=BLUE).move_to(
                    sink.get_center()
                    + np.array([np.cos(i * TAU / 4), np.sin(i * TAU / 4), 0]) * 0.4
                )
                for i in range(4)
            ]
        )

        # Source at soma
        source = Circle(radius=0.5, color=RED, fill_opacity=0.2, stroke_width=2)
        source.move_to(soma_center)
        plus_signs = VGroup(
            *[
                MathTex("+", font_size=20, color=RED).move_to(
                    source.get_center()
                    + np.array([np.cos(i * TAU / 4), np.sin(i * TAU / 4), 0]) * 0.35
                )
                for i in range(4)
            ]
        )

        # Dipole arrow
        dipole = Arrow(soma_center, dendrite_top, color=PURPLE, stroke_width=5, buff=0.5)

        return VGroup(neuron, sink, minus_signs, source, plus_signs, dipole)

    def create_snapshot_field(self):
        """Create snapshot showing electric field."""
        neuron = self.create_snapshot_neuron()
        soma_center = neuron[0].get_center()
        dendrite_top = neuron[2].get_end()

        # Simplified field lines
        field_lines = VGroup()
        for i in range(6):
            angle = i * TAU / 6
            start = soma_center + np.array([np.cos(angle), np.sin(angle), 0]) * 0.5
            control1 = start + np.array([np.cos(angle), np.sin(angle), 0]) * 1.2
            control2 = dendrite_top + np.array([np.cos(angle + PI), np.sin(angle + PI), 0]) * 0.8
            end = dendrite_top + np.array([np.cos(angle + PI), np.sin(angle + PI), 0]) * 0.6

            path = CubicBezier(start, control1, control2, end)
            field_line = path.set_color(GREEN).set_stroke(width=2, opacity=0.6)
            field_lines.add(field_line)

        # Dipole arrow (lighter)
        dipole = Arrow(
            soma_center,
            dendrite_top,
            color=PURPLE,
            stroke_width=4,
            buff=0.5,
            fill_opacity=0.5,
            stroke_opacity=0.5,
        )

        return VGroup(neuron, dipole, field_lines)


class ParallelNeuronsStatic(Scene):
    """Static comparison image of parallel vs random neuron arrangements."""

    def construct(self):
        # Left side: Parallel neurons - tighter spacing, centered
        left_label = Tex(r"\textbf{Parallel Neurons}", font_size=34, color=GREEN)
        left_label.move_to(LEFT * 2.3 + UP * 1.7)
        # Add subtle background box for readability
        left_bg = Rectangle(
            width=left_label.width + 0.3,
            height=left_label.height + 0.15,
            fill_color=BLACK,
            fill_opacity=0.7,
            stroke_width=0,
        ).move_to(left_label)
        self.add(left_bg, left_label)

        # Create 5 parallel neurons - tighter spacing
        parallel_neurons = VGroup()
        spacing = 0.45
        start_x = -2.3 - (spacing * 2)  # Center around -2.3
        for i in range(5):
            x_pos = start_x + (i * spacing)
            neuron = self.create_detailed_neuron(np.array([x_pos, -0.2, 0]), scale=0.4)
            parallel_neurons.add(neuron)

            # Add prominent charge distributions
            # Negative at dendrites (top)
            minus = MathTex("-", font_size=28, color=BLUE, stroke_width=2).move_to([x_pos, 1.2, 0])
            # Positive at soma (bottom)
            plus = MathTex("+", font_size=28, color=RED, stroke_width=2).move_to([x_pos, -0.9, 0])
            parallel_neurons.add(minus, plus)

        self.add(parallel_neurons)

        # Show summed dipole - shorter and thicker
        sum_arrow = Arrow(
            LEFT * 2.3 + DOWN * 1.5,
            LEFT * 2.3 + UP * 1.3,
            color=YELLOW,
            stroke_width=14,
            buff=0,
            max_tip_length_to_length_ratio=0.15,
        )
        sum_label = Tex(r"\textbf{Strong summed signal}", font_size=24, color=YELLOW)
        sum_label_bg = Rectangle(
            width=sum_label.width + 0.25,
            height=sum_label.height + 0.12,
            fill_color=BLACK,
            fill_opacity=0.7,
            stroke_width=0,
        )
        sum_label.next_to(sum_arrow, DOWN, buff=0.15)
        sum_label_bg.move_to(sum_label)
        self.add(sum_label_bg, sum_label, sum_arrow)

        # Vertical dividing line
        divider = Line(UP * 2.2, DOWN * 2.2, color=GRAY, stroke_width=2, stroke_opacity=0.3)
        self.add(divider)

        # Right side: Random neurons - more compact
        right_label = Tex(r"\textbf{Random Orientations}", font_size=34, color=RED)
        right_label.move_to(RIGHT * 2.3 + UP * 1.7)
        right_bg = Rectangle(
            width=right_label.width + 0.3,
            height=right_label.height + 0.15,
            fill_color=BLACK,
            fill_opacity=0.7,
            stroke_width=0,
        ).move_to(right_label)
        self.add(right_bg, right_label)

        # Create 5 random neurons - very tight cluster, smaller scale
        random_neurons = VGroup()
        angles = [PI / 2, PI / 6, -PI / 4, 2 * PI / 3, 0]
        # Tighter positions centered around RIGHT * 2.3
        positions = [
            [2.3, 0.3, 0],  # top center
            [1.9, -0.3, 0],  # left
            [2.7, -0.4, 0],  # right
            [2.0, -0.9, 0],  # bottom left
            [2.6, -1.0, 0],  # bottom right
        ]

        for i, (angle, pos) in enumerate(zip(angles, positions)):
            # Smaller neurons for tighter fit
            neuron = self.create_detailed_neuron(ORIGIN, scale=0.32, rotation=angle)
            neuron.move_to(pos)
            neuron.set_opacity(0.5)
            random_neurons.add(neuron)

            # More prominent charge indicators
            dendrite_offset = np.array([np.cos(angle), np.sin(angle), 0]) * 0.7
            soma_offset = np.array([np.cos(angle + PI), np.sin(angle + PI), 0]) * 0.32
            minus = MathTex("-", font_size=22, color=BLUE, stroke_width=2).move_to(
                np.array(pos) + dendrite_offset
            )
            plus = MathTex("+", font_size=22, color=RED, stroke_width=2).move_to(
                np.array(pos) + soma_offset
            )
            minus.set_opacity(0.5)
            plus.set_opacity(0.5)
            random_neurons.add(minus, plus)

        self.add(random_neurons)

        # Show cancellation - centered within cluster
        cancel_x = MathTex(r"\times", font_size=80, color=RED, stroke_width=3)
        cancel_x.move_to(RIGHT * 2.3 + DOWN * 1.5)
        cancel_label = Tex(r"\textbf{Signals cancel out}", font_size=24, color=RED)
        cancel_label_bg = Rectangle(
            width=cancel_label.width + 0.25,
            height=cancel_label.height + 0.12,
            fill_color=BLACK,
            fill_opacity=0.7,
            stroke_width=0,
        )
        cancel_label.next_to(cancel_x, DOWN, buff=0.15)
        cancel_label_bg.move_to(cancel_label)
        self.add(cancel_label_bg, cancel_label, cancel_x)

    def create_detailed_neuron(self, center, scale=1.0, rotation=0):
        """Create a more detailed pyramidal neuron."""
        # Soma (cell body) - larger and more visible
        soma = Circle(radius=0.18 * scale, color=BLUE, fill_opacity=0.4, stroke_width=3)

        # Apical dendrite trunk going up
        dendrite_trunk = Line(ORIGIN, UP * 1.8 * scale, color=BLUE, stroke_width=4)

        # Branching dendrites at top - more branches
        dendrite_top = dendrite_trunk.get_end()

        # Main branches
        branch1 = Line(
            dendrite_top,
            dendrite_top + (UP * 0.5 + LEFT * 0.35) * scale,
            color=BLUE,
            stroke_width=3,
        )
        branch2 = Line(
            dendrite_top,
            dendrite_top + (UP * 0.5 + RIGHT * 0.35) * scale,
            color=BLUE,
            stroke_width=3,
        )

        # Secondary branches
        branch1_end = branch1.get_end()
        branch1a = Line(
            branch1_end, branch1_end + (UP * 0.25 + LEFT * 0.15) * scale, color=BLUE, stroke_width=2
        )
        branch1b = Line(
            branch1_end, branch1_end + (UP * 0.3 + RIGHT * 0.1) * scale, color=BLUE, stroke_width=2
        )

        branch2_end = branch2.get_end()
        branch2a = Line(
            branch2_end,
            branch2_end + (UP * 0.25 + RIGHT * 0.15) * scale,
            color=BLUE,
            stroke_width=2,
        )
        branch2b = Line(
            branch2_end, branch2_end + (UP * 0.3 + LEFT * 0.1) * scale, color=BLUE, stroke_width=2
        )

        # Basal dendrites (smaller ones near soma)
        basal1 = Line(ORIGIN, (DOWN * 0.15 + LEFT * 0.25) * scale, color=BLUE, stroke_width=2)
        basal2 = Line(ORIGIN, (DOWN * 0.15 + RIGHT * 0.25) * scale, color=BLUE, stroke_width=2)

        # Axon going down
        axon = Line(ORIGIN, DOWN * 0.7 * scale, color=BLUE, stroke_width=3)

        neuron = VGroup(
            soma,
            dendrite_trunk,
            branch1,
            branch2,
            branch1a,
            branch1b,
            branch2a,
            branch2b,
            basal1,
            basal2,
            axon,
        )

        # Apply rotation if specified
        if rotation != 0:
            neuron.rotate(rotation)

        neuron.move_to(center)
        return neuron

    def create_simple_neuron(self, center, scale=1.0, rotation=0):
        """Create a simplified pyramidal neuron (for backwards compatibility)."""
        return self.create_detailed_neuron(center, scale, rotation)


class ParallelNeurons(Scene):
    """Show why parallel arrangement matters for EEG detection."""

    def construct(self):
        title = Tex(r"\textbf{Why Parallel Neurons Matter}", font_size=42)
        self.play(FadeIn(title, shift=UP * 0.3))
        self.wait(1)
        self.play(title.animate.to_edge(UP))

        # Show parallel neurons on left
        self.show_parallel_neurons()

        # Show random neurons on right
        self.show_random_neurons()

    def show_parallel_neurons(self):
        """Show parallel neurons with constructive summation."""
        label = Tex(r"Parallel Neurons", font_size=28, color=GREEN)
        label.shift(LEFT * 3.5 + UP * 2.5)

        self.play(FadeIn(label))

        # Create 5 simple dipoles (arrows) pointing same direction
        dipoles = VGroup()
        for i in range(5):
            arrow = Arrow(
                LEFT * 3.5 + DOWN * (2 - i * 0.8),
                LEFT * 3.5 + UP * (0.5 - i * 0.8),
                color=BLUE,
                stroke_width=4,
                buff=0,
            )
            dipoles.add(arrow)

        self.play(Create(dipoles), run_time=1.5)

        # Show summed field
        big_arrow = Arrow(
            LEFT * 3.5 + DOWN * 2.5, LEFT * 3.5 + UP * 1.5, color=YELLOW, stroke_width=8, buff=0
        )

        sum_label = Tex(r"Strong summed signal!", font_size=20, color=YELLOW)
        sum_label.next_to(big_arrow, LEFT, buff=0.3)

        self.wait(1)
        self.play(Transform(dipoles, big_arrow), FadeIn(sum_label))
        self.wait(1)

    def show_random_neurons(self):
        """Show random neurons with cancellation."""
        label = Tex(r"Random Orientations", font_size=28, color=RED)
        label.shift(RIGHT * 3.5 + UP * 2.5)

        self.play(FadeIn(label))

        # Create 5 dipoles pointing different directions
        dipoles = VGroup()
        angles = [0, PI / 3, -PI / 4, PI / 2, -PI / 3]

        for i, angle in enumerate(angles):
            start = RIGHT * 3.5 + DOWN * (2 - i * 0.8)
            end = start + np.array([np.cos(angle), np.sin(angle), 0]) * 2
            arrow = Arrow(start, end, color=BLUE, stroke_width=4, buff=0)
            dipoles.add(arrow)

        self.play(Create(dipoles), run_time=1.5)

        # Show they cancel
        cancel_x = MathTex(r"\times", font_size=80, color=RED)
        cancel_x.move_to(RIGHT * 3.5 + DOWN * 0.5)

        cancel_label = Tex(r"Signals cancel out!", font_size=20, color=RED)
        cancel_label.next_to(cancel_x, DOWN, buff=0.5)

        self.wait(1)
        self.play(dipoles.animate.set_opacity(0.3), FadeIn(cancel_x), FadeIn(cancel_label))
        self.wait(2)


if __name__ == "__main__":
    # Render with: manim -pql dipole_model.py DipoleModel
    pass
