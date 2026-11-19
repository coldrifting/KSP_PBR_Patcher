namespace TechnicolorPatcher.Types;

public struct TeamColor
{
    public string? Name { get; set; }
    public Vector4 Color { get; set; }
    public float Metalness { get; set; }
    public float Smoothness { get; set; }
    public float MetalBlend { get; set; }
    public float SmoothBlend { get; set; }
}

public static class TeamColorExt
{
    public static Tuple<TeamColor, TeamColor> GetTeamColors(string tc1, string? tc2)
    {
        TeamColor tc1Color = TeamColorDb[tc1];
        TeamColor tc2Color = tc2 != null ? TeamColorDb[tc2] : TeamColorDb[tc1];
        return new Tuple<TeamColor, TeamColor>(tc1Color, tc2Color);
    }
    
    public static Dictionary<string, TeamColor> TeamColorDb = new()
    {
        // Gloss
        {"porkjetWhite",     new TeamColor{ Name = "porkjetWhite",     Color = new Vector4(0.85f,   0.85f,    0.85f,  1), Metalness = 0, Smoothness = 0.75f, MetalBlend = 1, SmoothBlend = 1}},
        {"payloadGrey",      new TeamColor{ Name = "payloadGrey",      Color = new Vector4(0.65f,   0.65f,    0.65f,  1), Metalness = 0, Smoothness = 0.75f, MetalBlend = 1, SmoothBlend = 1}},
        {"porkjetGrey",      new TeamColor{ Name = "porkjetGrey",      Color = new Vector4(0.43f,   0.43f,    0.43f,  1), Metalness = 0, Smoothness = 0.75f, MetalBlend = 1, SmoothBlend = 1}},
        {"porkjetBlack",     new TeamColor{ Name = "porkjetBlack",     Color = new Vector4(0.05f,   0.05f,    0.05f,  1), Metalness = 0, Smoothness = 0.75f, MetalBlend = 1, SmoothBlend = 1}},
        {"electricalRed",    new TeamColor{ Name = "electricalRed",    Color = new Vector4(0.678f,  0.168f,   0.168f, 1), Metalness = 0, Smoothness = 0.75f, MetalBlend = 1, SmoothBlend = 1}},
        {"lithiumRed",       new TeamColor{ Name = "lithiumRed",       Color = new Vector4(0.67f,   0.25f,    0.20f,  1), Metalness = 0, Smoothness = 0.75f, MetalBlend = 1, SmoothBlend = 1}},
        {"intenseRed",       new TeamColor{ Name = "intenseRed",       Color = new Vector4(1.0f,    0.2f,     0.20f,  1), Metalness = 0, Smoothness = 0.75f, MetalBlend = 1, SmoothBlend = 1}},
        {"darkRed",          new TeamColor{ Name = "darkRed",          Color = new Vector4(0.34f,   0.07f,    0.07f,  1), Metalness = 0, Smoothness = 0.75f, MetalBlend = 1, SmoothBlend = 1}},
        {"mediumRed",        new TeamColor{ Name = "mediumRed",        Color = new Vector4(0.74f,   0.18f,    0.18f,  1), Metalness = 0, Smoothness = 0.75f, MetalBlend = 1, SmoothBlend = 1}},
        {"rockomaxOrange",   new TeamColor{ Name = "rockomaxOrange",   Color = new Vector4(0.832f,  0.456f,   0.201f, 1), Metalness = 0, Smoothness = 0.75f, MetalBlend = 1, SmoothBlend = 1}},
        {"kerbodyneOrange",  new TeamColor{ Name = "kerbodyneOrange",  Color = new Vector4(0.745f,  0.39f,    0.123f, 1), Metalness = 0, Smoothness = 0.75f, MetalBlend = 1, SmoothBlend = 1}},
        {"atomicOrange",     new TeamColor{ Name = "atomicOrange",     Color = new Vector4(0.881f,  0.5588f,  0.142f, 1), Metalness = 0, Smoothness = 0.75f, MetalBlend = 1, SmoothBlend = 1}},
        {"drogueOrange",     new TeamColor{ Name = "drogueOrange",     Color = new Vector4(1.0f,    0.52f,    0.2f,   1), Metalness = 0, Smoothness = 0.75f, MetalBlend = 1, SmoothBlend = 1}},
        {"jebsYellow",       new TeamColor{ Name = "jebsYellow",       Color = new Vector4(0.965f,  0.741f,   0.08f,  1), Metalness = 0, Smoothness = 0.75f, MetalBlend = 1, SmoothBlend = 1}},
        {"electricalYellow", new TeamColor{ Name = "electricalYellow", Color = new Vector4(0.852f,  0.6707f,  0.214f, 1), Metalness = 0, Smoothness = 0.75f, MetalBlend = 1, SmoothBlend = 1}},
        {"intenseYellow",    new TeamColor{ Name = "intenseYellow",    Color = new Vector4(1.0f,    0.98f,    0.20f,  1), Metalness = 0, Smoothness = 0.75f, MetalBlend = 1, SmoothBlend = 1}},
        {"darkYellow",       new TeamColor{ Name = "darkYellow",       Color = new Vector4(0.34f,   0.35f,    0.07f,  1), Metalness = 0, Smoothness = 0.75f, MetalBlend = 1, SmoothBlend = 1}},
        {"mediumYellow",     new TeamColor{ Name = "mediumYellow",     Color = new Vector4(0.847f,  0.83f,    0.211f, 1), Metalness = 0, Smoothness = 0.75f, MetalBlend = 1, SmoothBlend = 1}},
        {"deltaGreen",       new TeamColor{ Name = "deltaGreen",       Color = new Vector4(0.553f,  0.613f,   0.373f, 1), Metalness = 0, Smoothness = 0.75f, MetalBlend = 1, SmoothBlend = 1}},
        {"sovietGreen",      new TeamColor{ Name = "sovietGreen",      Color = new Vector4(0.334f,  0.367f,   0.334f, 1), Metalness = 0, Smoothness = 0.75f, MetalBlend = 1, SmoothBlend = 1}},
        {"methaneGreen",     new TeamColor{ Name = "methaneGreen",     Color = new Vector4(0.372f,  0.518f,   0.340f, 1), Metalness = 0, Smoothness = 0.75f, MetalBlend = 1, SmoothBlend = 1}},
        {"heliumGreen",      new TeamColor{ Name = "heliumGreen",      Color = new Vector4(0.32f,   0.467f,   0.454f, 1), Metalness = 0, Smoothness = 0.75f, MetalBlend = 1, SmoothBlend = 1}},
        {"intenseGreen",     new TeamColor{ Name = "intenseGreen",     Color = new Vector4(0.2f,    1.0f,     0.20f,  1), Metalness = 0, Smoothness = 0.75f, MetalBlend = 1, SmoothBlend = 1}},
        {"darkGreen",        new TeamColor{ Name = "darkGreen",        Color = new Vector4(0.07f,   0.34f,    0.07f,  1), Metalness = 0, Smoothness = 0.75f, MetalBlend = 1, SmoothBlend = 1}},
        {"mediumGreen",      new TeamColor{ Name = "mediumGreen",      Color = new Vector4(0.18f,   0.74f,    0.18f,  1), Metalness = 0, Smoothness = 0.75f, MetalBlend = 1, SmoothBlend = 1}},
        {"intenseCyan",      new TeamColor{ Name = "intenseCyan",      Color = new Vector4(0.2f,    0.96f,    1.0f,   1), Metalness = 0, Smoothness = 0.75f, MetalBlend = 1, SmoothBlend = 1}},
        {"darkCyan",         new TeamColor{ Name = "darkCyan",         Color = new Vector4(0.07f,   0.34f,    0.35f,  1), Metalness = 0, Smoothness = 0.75f, MetalBlend = 1, SmoothBlend = 1}},
        {"mediumCyan",       new TeamColor{ Name = "mediumCyan",       Color = new Vector4(0.21f,   0.815f,   0.85f,  1), Metalness = 0, Smoothness = 0.75f, MetalBlend = 1, SmoothBlend = 1}},
        {"chuteBlue ",       new TeamColor{ Name = "chuteBlue",        Color = new Vector4(0.32f,   0.537f,   0.76f,  1), Metalness = 0, Smoothness = 0.75f, MetalBlend = 1, SmoothBlend = 1}},
        {"electricalBlue",   new TeamColor{ Name = "electricalBlue",   Color = new Vector4(0.149f,  0.203f,   0.6f,   1), Metalness = 0, Smoothness = 0.75f, MetalBlend = 1, SmoothBlend = 1}},
        {"scienceBlue",      new TeamColor{ Name = "scienceBlue",      Color = new Vector4(0.1329f, 0.629f,   0.801f, 1), Metalness = 0, Smoothness = 0.75f, MetalBlend = 1, SmoothBlend = 1}},
        {"deltaBlue",        new TeamColor{ Name = "deltaBlue",        Color = new Vector4(0.278f,  0.419f,   0.458f, 1), Metalness = 0, Smoothness = 0.75f, MetalBlend = 1, SmoothBlend = 1}},
        {"hydrogenBlue",     new TeamColor{ Name = "hydrogenBlue",     Color = new Vector4(0.361f,  0.521f,   0.575f, 1), Metalness = 0, Smoothness = 0.75f, MetalBlend = 1, SmoothBlend = 1}},
        {"deuteriumBlue",    new TeamColor{ Name = "deuteriumBlue",    Color = new Vector4(0.40f,   0.453f,   0.566f, 1), Metalness = 0, Smoothness = 0.75f, MetalBlend = 1, SmoothBlend = 1}},
        {"antimatterBlue",   new TeamColor{ Name = "antimatterBlue",   Color = new Vector4(0.230f,  0.467f,   0.650f, 1), Metalness = 0, Smoothness = 0.75f, MetalBlend = 1, SmoothBlend = 1}},
        {"argonBlue",        new TeamColor{ Name = "argonBlue",        Color = new Vector4(0.321f,  0.465f,   0.603f, 1), Metalness = 0, Smoothness = 0.75f, MetalBlend = 1, SmoothBlend = 1}},
        {"intenseBlue",      new TeamColor{ Name = "intenseBlue",      Color = new Vector4(0.2f,    0.2f,     1.0f,   1), Metalness = 0, Smoothness = 0.75f, MetalBlend = 1, SmoothBlend = 1}},
        {"darkBlue",         new TeamColor{ Name = "darkBlue",         Color = new Vector4(0.07f,   0.07f,    0.34f,  1), Metalness = 0, Smoothness = 0.75f, MetalBlend = 1, SmoothBlend = 1}},
        {"mediumBlue",       new TeamColor{ Name = "mediumBlue",       Color = new Vector4(0.18f,   0.18f,    0.74f,  1), Metalness = 0, Smoothness = 0.75f, MetalBlend = 1, SmoothBlend = 1}},
        {"intensePurple",    new TeamColor{ Name = "intensePurple",    Color = new Vector4(0.57f,   0.2f,     1.0f,   1), Metalness = 0, Smoothness = 0.75f, MetalBlend = 1, SmoothBlend = 1}},
        {"darkPurple",       new TeamColor{ Name = "darkPurple",       Color = new Vector4(0.51f,   0.07f,    0.35f,  1), Metalness = 0, Smoothness = 0.75f, MetalBlend = 1, SmoothBlend = 1}},
        {"mediumPurple",     new TeamColor{ Name = "mediumPurple",     Color = new Vector4(0.2f,    0.07f,    0.34f,  1), Metalness = 0, Smoothness = 0.75f, MetalBlend = 1, SmoothBlend = 1}},
        
        // Matte
        {"dullWhite",       new TeamColor{ Name = "dullWhite",       Color = new Vector4(0.85f,  0.85f,  0.85f,  1), Metalness = 0,    Smoothness = 0.35f, MetalBlend = 1, SmoothBlend = 1}},
        {"melancholyWhite", new TeamColor{ Name = "melancholyWhite", Color = new Vector4(0.65f,  0.65f,  0.65f,  1), Metalness = 0,    Smoothness = 0.35f, MetalBlend = 1, SmoothBlend = 1}},
        {"cloudGrey",       new TeamColor{ Name = "cloudGrey",       Color = new Vector4(0.427f, 0.427f, 0.427f, 1), Metalness = 0,    Smoothness = 0.35f, MetalBlend = 1, SmoothBlend = 1}},
        {"tileBlack",       new TeamColor{ Name = "tileBlack",       Color = new Vector4(0.05f,  0.05f,  0.05f,  1), Metalness = 0,    Smoothness = 0.35f, MetalBlend = 1, SmoothBlend = 1}},                                                                                                                                                    
        
        // Metallic
        {"metalBasic",      new TeamColor{ Name = "metalBasic",      Color = new Vector4(0.5f,   0.5f,   0.5f,   1), Metalness = 1,    Smoothness = 0.9f,  MetalBlend = 0, SmoothBlend = 0}},
        {"metalBlack",      new TeamColor{ Name = "metalBlack",      Color = new Vector4(0.1f,   0.1f,   0.1f,   1), Metalness = 1,    Smoothness = 0.9f,  MetalBlend = 0, SmoothBlend = 0}},
        {"metalDarkGrey",   new TeamColor{ Name = "metalDarkGrey",   Color = new Vector4(0.35f,  0.35f,  0.35f,  1), Metalness = 1,    Smoothness = 0.9f,  MetalBlend = 0, SmoothBlend = 0}},
        {"metalShiny",      new TeamColor{ Name = "metalShiny",      Color = new Vector4(0.7f,   0.7f,   0.7f,   1), Metalness = 1,    Smoothness = 0.9f,  MetalBlend = 0, SmoothBlend = 0}},
        {"metalCopper",     new TeamColor{ Name = "metalCopper",     Color = new Vector4(0.839f, 0.617f, 0.439f, 1), Metalness = 1,    Smoothness = 0.9f,  MetalBlend = 0, SmoothBlend = 0}},
        {"metalGold",       new TeamColor{ Name = "metalGold",       Color = new Vector4(0.96f,  0.76f,  0.356f, 1), Metalness = 1,    Smoothness = 0.9f,  MetalBlend = 0, SmoothBlend = 0}},
        {"metalBrass",      new TeamColor{ Name = "metalBrass",      Color = new Vector4(0.858f, 0.75f,  0.627f, 1), Metalness = 1,    Smoothness = 0.9f,  MetalBlend = 0, SmoothBlend = 0}},
        {"metalBluish",     new TeamColor{ Name = "metalBluish",     Color = new Vector4(0.541f, 0.583f, 0.594f, 1), Metalness = 1,    Smoothness = 0.9f,  MetalBlend = 0, SmoothBlend = 0}},                                         
        
        // MLI
        {"mliGold",         new TeamColor{ Name = "mliGold",         Color = new Vector4(0.915f, 0.751f, 0.33f,  1), Metalness = 0.7f, Smoothness = 1,     MetalBlend = 0, SmoothBlend = 0}},
        {"mliSilver",       new TeamColor{ Name = "mliSilver",       Color = new Vector4(0.75f,  0.75f,  0.75f,  1), Metalness = 0.7f, Smoothness = 1,     MetalBlend = 0, SmoothBlend = 0}},
        {"mliBlack",        new TeamColor{ Name = "mliBlack",        Color = new Vector4(0.05f,  0.05f,  0.05f,  1), Metalness = 0.7f, Smoothness = 1,     MetalBlend = 0, SmoothBlend = 0}},                                                                                                                                                               
        
        // SOFI Insulation
        {"sofiOrange",      new TeamColor{ Name = "sofiOrange",      Color = new Vector4(0.832f, 0.456f, 0.201f, 1), Metalness = 0,    Smoothness = 0.2f,  MetalBlend = 1, SmoothBlend = 1}},
        {"sofiYellow",      new TeamColor{ Name = "sofiYellow",      Color = new Vector4(0.990f, 0.655f, 0.228f, 1), Metalness = 0,    Smoothness = 0.2f,  MetalBlend = 1, SmoothBlend = 1}},
        {"sofiBlue",        new TeamColor{ Name = "sofiBlue",        Color = new Vector4(0.176f, 0.423f, 0.49f,  1), Metalness = 0,    Smoothness = 0.2f,  MetalBlend = 1, SmoothBlend = 1}},
        {"sofiBrown",       new TeamColor{ Name = "sofiBrown",       Color = new Vector4(0.575f, 0.49f,  0.37f,  1), Metalness = 0,    Smoothness = 0.2f,  MetalBlend = 1, SmoothBlend = 1}},
        {"sofiBeige",       new TeamColor{ Name = "sofiBeige",       Color = new Vector4(0.745f, 0.711f, 0.657f, 1), Metalness = 0,    Smoothness = 0.2f,  MetalBlend = 1, SmoothBlend = 1}},
        {"sofiWhite",       new TeamColor{ Name = "sofiWhite",       Color = new Vector4(0.8f,   0.8f,   0.8f,   1), Metalness = 0,    Smoothness = 0.2f,  MetalBlend = 1, SmoothBlend = 1}},                                                      
        
        // Plastic
        {"plasticWhite",    new TeamColor{ Name = "plasticWhite",    Color = new Vector4(0.95f,  0.95f,  0.95f,  1), Metalness = 0,    Smoothness = 1,     MetalBlend = 1, SmoothBlend = 0.3f}},
        {"plasticBlack",    new TeamColor{ Name = "plasticBlack",    Color = new Vector4(0.05f,  0.05f,  0.05f,  1), Metalness = 0,    Smoothness = 1,     MetalBlend = 1, SmoothBlend = 0.3f}},
        {"plasticYellow",   new TeamColor{ Name = "plasticYellow",   Color = new Vector4(0.915f, 0.715f, 0.211f, 1), Metalness = 0,    Smoothness = 1,     MetalBlend = 1, SmoothBlend = 0.3f}},
        {"plasticRed",      new TeamColor{ Name = "plasticRed",      Color = new Vector4(0.698f, 0.119f, 0.101f, 1), Metalness = 0,    Smoothness = 1,     MetalBlend = 1, SmoothBlend = 0.3f}},
        {"plasticBlue",     new TeamColor{ Name = "plasticBlue",     Color = new Vector4(0.102f, 0.153f, 0.698f, 1), Metalness = 0,    Smoothness = 1,     MetalBlend = 1, SmoothBlend = 0.3f}},                                                                                                                                                                
        
        // Fabric Insulation
        {"blanketWhite",    new TeamColor{ Name = "blanketWhite",    Color = new Vector4(0.85f,  0.85f,  0.85f,  1), Metalness = 0,    Smoothness = 0.3f,  MetalBlend = 1, SmoothBlend = 1}},
        {"blanketBeige",    new TeamColor{ Name = "blanketBeige",    Color = new Vector4(0.8f,   0.786f, 0.766f, 1), Metalness = 0,    Smoothness = 0.3f,  MetalBlend = 1, SmoothBlend = 1}},
        {"blanketBlack",    new TeamColor{ Name = "blanketBlack",    Color = new Vector4(0.05f,  0.05f,  0.05f,  1), Metalness = 0,    Smoothness = 0.3f,  MetalBlend = 1, SmoothBlend = 1}},
    };
}