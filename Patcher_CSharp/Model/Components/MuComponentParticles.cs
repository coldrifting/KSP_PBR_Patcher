using System.Numerics;
using KSP_PBR_Patcher.Model.IO;
using KSP_PBR_Patcher.Model.Tags;

namespace KSP_PBR_Patcher.Model.Components;

public class MuComponentParticles : IMuComponent
{
    public bool Emit { get; set; }
    public int Shape { get; set; }
    public Vector3 Shape3d { get; set; }
    public Vector2 Shape2d { get; set; }
    public float Shape1d { get; set; }
    public Vector4 Color { get; set; }
    public bool UseWorldSpace { get; set; }
    public Vector2 SizeMinMax { get; set; }
    public Vector2 EnergyMinMax { get; set; }
    public Vector2 EmissionMinMax { get; set; }
    public Vector3 VelocityWorld { get; set; }
    public Vector3 VelocityLocal { get; set; }
    public Vector3 VelocityRandom { get; set; }
    public float VelocityEmitScale { get; set; }
    public float VelocityAngular { get; set; }
    public float VelocityAngularRandom { get; set; }
    public bool RotationRandom { get; set; }
    public bool AnimateColor { get; set; }
    public required Vector4[] ColorAnimations { get; set; }
    public Vector3 AxisRotationWorld { get; set; }
    public Vector3 AxisRotationLocal { get; set; }
    public float SizeGrow { get; set; }
    public Vector3 ForceRandom { get; set; }
    public Vector3 Force { get; set; }
    public float Damping { get; set; }
    public bool ShadowCast { get; set; }
    public bool ShadowReceive { get; set; }
    public float ScaleLength { get; set; }
    public float ScaleVelocity { get; set; }
    public float MaxParticleSize { get; set; }
    public int ParticleRenderMode { get; set; }
    public Vector3 UvAnimation { get; set; } // xtile, ytile, cycles
    public int Count { get; set; }

    public static MuComponentParticles Read(MuReader reader)
    {
        bool emit = reader.ReadBoolean();
        int shape = reader.ReadInt32();
        Vector3 shape3d = reader.ReadVec3();
        Vector2 shape2d = reader.ReadVec2();
        float shape1d = reader.ReadSingle();
        Vector4 color = reader.ReadVec4();
        bool useWorldSpace = reader.ReadBoolean();
        Vector2 sizeMinMax = reader.ReadVec2();
        Vector2 energyMinMax = reader.ReadVec2();
        Vector2 emissionMinMax = reader.ReadVec2();
        Vector3 velocityWorld = reader.ReadVec3();
        Vector3 velocityLocal = reader.ReadVec3();
        Vector3 velocityRandom = reader.ReadVec3();
        float velocityEmitScale = reader.ReadSingle();
        float velocityAngular = reader.ReadSingle();
        float velocityAngularRandom = reader.ReadSingle();
        bool rotationRandom = reader.ReadBoolean();
        bool animateColor = reader.ReadBoolean();

        const int numColorAnimations = 5;
        Vector4[] colorAnimations = new Vector4[numColorAnimations];
        for (int i = 0; i < numColorAnimations; i++)
        {
            colorAnimations[i] = reader.ReadVec4();
        }

        Vector3 axisRotationWorld = reader.ReadVec3();
        Vector3 axisRotationLocal = reader.ReadVec3();
        float sizeGrow = reader.ReadSingle();
        Vector3 forceRandom = reader.ReadVec3();
        Vector3 force = reader.ReadVec3();
        float damping = reader.ReadSingle();
        bool shadowCast = reader.ReadBoolean();
        bool shadowReceive = reader.ReadBoolean();
        float scaleLength = reader.ReadSingle();
        float scaleVelocity = reader.ReadSingle();
        float maxParticleSize = reader.ReadSingle();
        int particleRenderMode = reader.ReadInt32();
        Vector3 uvAnimation = reader.ReadVec3();
        int count = reader.ReadInt32();

        return new MuComponentParticles
        {
            Emit = emit,
            Shape = shape,
            Shape3d = shape3d,
            Shape2d = shape2d,
            Shape1d = shape1d,
            Color = color,
            UseWorldSpace = useWorldSpace,
            SizeMinMax = sizeMinMax,
            EnergyMinMax = energyMinMax,
            EmissionMinMax = emissionMinMax,
            VelocityWorld = velocityWorld,
            VelocityLocal = velocityLocal,
            VelocityRandom = velocityRandom,
            VelocityEmitScale = velocityEmitScale,
            VelocityAngular = velocityAngular,
            VelocityAngularRandom = velocityAngularRandom,
            RotationRandom = rotationRandom,
            AnimateColor = animateColor,
            ColorAnimations = colorAnimations,
            AxisRotationWorld = axisRotationWorld,
            AxisRotationLocal = axisRotationLocal,
            SizeGrow = sizeGrow,
            ForceRandom = forceRandom,
            Force = force,
            Damping = damping,
            ShadowCast = shadowCast,
            ShadowReceive = shadowReceive,
            ScaleLength = scaleLength,
            ScaleVelocity = scaleVelocity,
            MaxParticleSize = maxParticleSize,
            ParticleRenderMode = particleRenderMode,
            UvAnimation = uvAnimation,
            Count = count
        };
    }

    public void Write(BinaryWriter writer)
    {
        writer.Write(MuTag.Particles);

        writer.Write(Emit);
        writer.Write(Shape);
        writer.Write(Shape3d);
        writer.Write(Shape2d);
        writer.Write(Shape1d);
        writer.Write(Color);
        writer.Write(UseWorldSpace);
        writer.Write(SizeMinMax);
        writer.Write(EnergyMinMax);
        writer.Write(EmissionMinMax);
        writer.Write(VelocityWorld);
        writer.Write(VelocityLocal);
        writer.Write(VelocityRandom);
        writer.Write(VelocityEmitScale);
        writer.Write(VelocityAngular);
        writer.Write(VelocityAngularRandom);
        writer.Write(RotationRandom);
        writer.Write(AnimateColor);
    
        // Hardcoded to length of 5, no need to prefix length
        foreach (Vector4 colorAnimation in ColorAnimations)
        {
            writer.Write(colorAnimation);
        }

        writer.Write(AxisRotationWorld);
        writer.Write(AxisRotationLocal);
        writer.Write(SizeGrow);
        writer.Write(ForceRandom);
        writer.Write(Force);
        writer.Write(Damping);
        writer.Write(ShadowCast);
        writer.Write(ShadowReceive);
        writer.Write(ScaleLength);
        writer.Write(ScaleVelocity);
        writer.Write(MaxParticleSize);
        writer.Write(ParticleRenderMode);
        writer.Write(UvAnimation);
        writer.Write(Count);
    }

    public IMuComponent Clone()
    {
        return new MuComponentParticles
        {
            Emit = Emit,
            Shape = Shape,
            Shape3d = Shape3d,
            Shape2d = Shape2d,
            Shape1d = Shape1d,
            Color = Color,
            UseWorldSpace = UseWorldSpace,
            SizeMinMax = SizeMinMax,
            EnergyMinMax = EnergyMinMax,
            EmissionMinMax = EmissionMinMax,
            VelocityWorld = VelocityWorld,
            VelocityLocal = VelocityLocal,
            VelocityRandom = VelocityRandom,
            VelocityEmitScale = VelocityEmitScale,
            VelocityAngular = VelocityAngular,
            VelocityAngularRandom = VelocityAngularRandom,
            RotationRandom = RotationRandom,
            AnimateColor = AnimateColor,
            ColorAnimations = ColorAnimations.Select(c => c).ToArray(),
            AxisRotationWorld = AxisRotationWorld,
            AxisRotationLocal = AxisRotationLocal,
            SizeGrow = SizeGrow,
            ForceRandom = ForceRandom,
            Force = Force,
            Damping = Damping,
            ShadowCast = ShadowCast,
            ShadowReceive = ShadowReceive,
            ScaleLength = ScaleLength,
            ScaleVelocity = ScaleVelocity,
            MaxParticleSize = MaxParticleSize,
            ParticleRenderMode = ParticleRenderMode,
            UvAnimation = UvAnimation,
            Count = Count
        };
    }
}