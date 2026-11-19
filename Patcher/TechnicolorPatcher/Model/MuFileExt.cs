using TechnicolorPatcher.Model.Components;
using TechnicolorPatcher.Model.Components.Material;
using TechnicolorPatcher.Model.Tags;
using TechnicolorPatcher.Types;

namespace TechnicolorPatcher.Model;

public static class MuFileExt
{
    extension(MuFile muFile)
    {
        public List<MuTransform> GetTransforms(string? transformName, MuTag tag)
        {
            return muFile.GetTransforms(transformName, [tag]);
        }

        public List<MuTransform> GetTransforms(string? transformName, HashSet<MuTag>? tags = null)
        {
            List<MuTransform> output = [];
            
            Queue<MuTransform> queue = new();
            queue.Enqueue(muFile.RootTransform);

            while (queue.Count > 0)
            {
                MuTransform transform = queue.Dequeue();
                if (transformName == null || transform.Name == transformName)
                {
                    if (tags == null || tags.Count == 0)
                    {
                        output.Add(transform);
                    }
                    else
                    {
                        foreach (MuTag tag in tags)
                        {
                            if (transform.Data.ContainsKey(tag))
                            {
                                output.Add(transform);
                                break;
                            }
                        }
                    }
                }

                foreach (MuTransform child in transform.Children)
                {
                    queue.Enqueue(child);
                }
            }

            return output;
        }

        public MuTransform CopyTransform(string transform, string newName, string model, string gameDataPath)
        {
            MuFile inputFile = MuFile.ReadFile(Path.Combine(gameDataPath, model) + ".mu");
            List<MuTransform> transforms = inputFile.GetTransforms(transform);
            if (transforms.Count == 0)
            {
                throw new ArgumentException($"Unable to find transform with name {transform} in model file {model}");
            }

            transforms[0].Name = newName;
            int materialIndex;
            if (transforms[0].Data.ContainsKey(MuTag.MeshRenderer))
            {
                MuComponentRenderer renderer = (MuComponentRenderer)transforms[0][MuTag.MeshRenderer];
                materialIndex = renderer.MaterialIndex;
            }
            else if (transforms[0].Data.ContainsKey(MuTag.SkinnedMeshRenderer))
            {
                MuComponentSkinnedMesh skinnedMesh = (MuComponentSkinnedMesh)transforms[0][MuTag.SkinnedMeshRenderer];
                materialIndex = skinnedMesh.MaterialIndices[0];
            }
            else
            {
                materialIndex = -1;
            }
            
            if (materialIndex != -1)
            {
                Material material = inputFile.Materials[materialIndex];
                
                foreach (IProperty materialProperty in material.Properties)
                {
                    if (materialProperty is PropertyTexture textureProperty)
                    {
                        MuTexture texture = inputFile.Textures[textureProperty.TextureIndex];
                        muFile.Textures.Add(texture);
                        textureProperty.TextureIndex = muFile.Textures.Count - 1;
                    }
                }

                muFile.Materials.Add(material);

                MuFile.AssignMaterial(transforms[0], muFile.Materials.Count - 1);
            }
            
            muFile.RootTransform.Children.Add(transforms[0]);
            return transforms[0];
        }
        
        public MuTransform CopyTransform(MuTransform transform, string newName)
        {
            if (muFile.RootTransform.Name == transform.Name)
            {
                throw new ArgumentException("Cannot copy root transform");
            }
            
            Queue<List<MuTransform>> queue = new();
            queue.Enqueue(muFile.RootTransform.Children);

            while (queue.Count > 0)
            {
                List<MuTransform> muTransforms = queue.Dequeue();
                for (int i = 0; i < muTransforms.Count; i++)
                {
                    MuTransform child = muTransforms[i];
                    if (child.Name == transform.Name)
                    {
                        MuTransform copy = child.Clone();
                        copy.Name = newName;
                        muTransforms.Add(copy);
                        return copy;
                    }

                    queue.Enqueue(child.Children);
                }
            }
            
            throw new ArgumentException($"No Transforms were found with the name {transform.Name}");
        }

        public Material GetMaterial(string materialName)
        {
            int index = muFile.GetMaterialIndex(materialName);
            return index == -1 
                ? throw new ArgumentException($"Material {materialName} not found") 
                : muFile.Materials[index];
        }

        public int GetMaterialIndex(string materialName)
        {
            return muFile.Materials.Select(m => m.Name).ToList().IndexOf(materialName);
        }

        public void CopyMaterial(Material material, string newMaterialName)
        {
            Material newMat = material.Clone();
            newMat.Name = newMaterialName;
            muFile.Materials.Add(newMat);
        }

        public static void AssignMaterial(MuTransform transform, int materialIndex)
        {
            if (transform.Data.ContainsKey(MuTag.MeshRenderer))
            {
                MuComponentRenderer renderer = (MuComponentRenderer)transform[MuTag.MeshRenderer];
                renderer.MaterialIndex = materialIndex;
            }
            else if (transform.Data.ContainsKey(MuTag.SkinnedMeshRenderer))
            {
                MuComponentSkinnedMesh skinnedMesh = (MuComponentSkinnedMesh)transform[MuTag.SkinnedMeshRenderer];
                skinnedMesh.MaterialIndices[0] = materialIndex;
            }
        }

        public MuTexture GetTexture(string texture)
        {
            string textureWithoutExt = Path.GetFileNameWithoutExtension(texture);
            return muFile.Textures.First(t => Path.GetFileNameWithoutExtension(t.Name) == textureWithoutExt);
        }

        public int GetTextureIndex(string texture)
        {
            string textureWithoutExt = Path.GetFileNameWithoutExtension(texture);
            return muFile.Textures.Select(t => Path.GetFileNameWithoutExtension(t.Name)).ToList().IndexOf(textureWithoutExt);
        }

        public void AddTextureMap(string materialName, string propName, string textureName, Vector2 scale, Vector2 offset)
        {
            muFile.AddTextureMap(muFile.Materials.First(m => m.Name == materialName), propName, textureName, scale, offset);
        }

        public void AddTextureMap(Material material, string propName, string textureName, Vector2 scale, Vector2 offset)
        {
            muFile.Textures.Add(new MuTexture
            {
                Name = textureName,
                IsNormalMap = propName == "_BumpMap"
            });

            PropertyTexture textureProp = new()
            {
                Name = propName,
                TextureIndex = muFile.Textures.Count - 1,
                TextureScale = scale,
                TextureOffset = offset
            };

            material.Properties.Add(textureProp);
        }

        public void EditTextureMap(Material material, string propName, string textureName, Vector2 scale, Vector2 offset)
        {
            int index = muFile.Textures.Select(t => t.Name).ToList().IndexOf(textureName);
            if (index == -1)
            {
                muFile.Textures.Add(new MuTexture
                {
                    Name = textureName,
                    IsNormalMap = propName == "_BumpMap"
                });
                index = muFile.Textures.Count - 1;
            }
            
            PropertyTexture textureProp = new()
            {
                Name = propName,
                TextureIndex = index,
                TextureScale = scale,
                TextureOffset = offset
            };

            material.Properties.Add(textureProp);
        }

        public void AssignTeamColors(string materialName, TeamColor tc1, TeamColor tc2)
        {
            Material material = muFile.GetMaterial(materialName);
            if (material.ShaderName != "Resurfaced/Standard (TC)")
            {
                material.ShaderName = "Resurfaced/Standard (TC)";

                PropertyTexture mainTexProp = (PropertyTexture)material.Properties
                    .First(p => p.Name == "_MainTex");

                string mainTexFileName = Path.GetFileNameWithoutExtension(muFile.Textures[mainTexProp.TextureIndex].Name);
                if (!mainTexFileName.EndsWith("-a"))
                {
                    muFile.Textures[mainTexProp.TextureIndex].Name = mainTexFileName + "-a";
                }

                IProperty? bumpProp = material.Properties.FirstOrDefault(p => p.Name == "_BumpMap");
                if (bumpProp is null)
                {
                    muFile.AddTextureMap(material, "_BumpMap", mainTexFileName + "-n", mainTexProp.TextureScale, mainTexProp.TextureOffset);
                }
                
                muFile.AddTextureMap(material, "_MetalMap", mainTexFileName + "-m", mainTexProp.TextureScale, mainTexProp.TextureOffset);
                muFile.AddTextureMap(material, "_TeamColorMap", mainTexFileName + "-tc", mainTexProp.TextureScale, mainTexProp.TextureOffset);

                material.Properties = material.Properties.Where(p => p.Name != "_SpecMap").ToList();
            }

            material.AddOrUpdateProperty("_TC1Color", tc1.Color);
            material.AddOrUpdateProperty("_TC1Metalness", tc1.Metalness);
            material.AddOrUpdateProperty("_TC1Smoothness", tc1.Smoothness);
            material.AddOrUpdateProperty("_TC1MetalBlend", tc1.MetalBlend);
            material.AddOrUpdateProperty("_TC1SmoothBlend", tc1.SmoothBlend);

            material.AddOrUpdateProperty("_TC2Color", tc2.Color);
            material.AddOrUpdateProperty("_TC2Metalness", tc2.Metalness);
            material.AddOrUpdateProperty("_TC2Smoothness", tc2.Smoothness);
            material.AddOrUpdateProperty("_TC2MetalBlend", tc2.MetalBlend);
            material.AddOrUpdateProperty("_TC2SmoothBlend", tc2.SmoothBlend);
        }

        public void CopyTriangles(MuTransform source, MuTransform? destination, List<int> triangleIndices)
        {
            MuComponentMesh meshSource = (MuComponentMesh)source[MuTag.MeshFilter];
            
            List<Int3> splitTrianglesTemp = [];
            foreach (int index in triangleIndices)
            {
                splitTrianglesTemp.Add(meshSource.Triangles[index]);
            }

            HashSet<int> usedVertexIndices = [];
            foreach (Int3 triangle in splitTrianglesTemp)
            {
                usedVertexIndices.Add(triangle.X);
                usedVertexIndices.Add(triangle.Y);
                usedVertexIndices.Add(triangle.Z);
            }

            List<VertexData> splitVertexData = [];
            Dictionary<int, int> mapping = [];
            int newIndex = 0;
            for (int index = 0; index < meshSource.VertexData.Length; index++)
            {
                if (usedVertexIndices.Contains(index))
                {
                    splitVertexData.Add(meshSource.VertexData[index].Clone());
                    mapping[index] = newIndex;
                    newIndex++;
                }
            }

            List<Int3> splitTriangles = [];
            foreach (Int3 triangle in splitTrianglesTemp)
            {
                splitTriangles.Add(new Int3(
                    mapping[triangle.X],  
                    mapping[triangle.Y], 
                    mapping[triangle.Z]));
            }

            if (destination is null)
            {
                int offset = meshSource.VertexData.Length;
                for (int i = 0; i < splitTriangles.Count; i++)
                {
                    splitTriangles[i] = new Int3(
                        splitTriangles[i].X + offset,
                        splitTriangles[i].Y + offset,
                        splitTriangles[i].Z + offset
                    );
                }

                meshSource.VertexData = meshSource.VertexData.Concat(splitVertexData).ToArray();
                meshSource.Triangles = meshSource.Triangles.Concat(splitTriangles).ToArray();
            }
            else
            {
                MuComponentMesh meshDest = (MuComponentMesh)destination[MuTag.MeshFilter];
                int destNumVertices = meshDest.VertexData.Length;
                for (int i = 0; i < splitTriangles.Count; i++)
                {
                    splitTriangles[i] = new Int3(
                        splitTriangles[i].X + destNumVertices,
                        splitTriangles[i].Y + destNumVertices,
                        splitTriangles[i].Z + destNumVertices);
                }
                
                meshDest.VertexData = meshSource.VertexData.Concat(splitVertexData).ToArray();
                meshDest.Triangles = meshSource.Triangles.Concat(splitTriangles).ToArray();
            }
        }

        public static void RemoveTriangles(MuTransform source, List<int> triangleIndices)
        {
            MuComponentMesh meshSource = (MuComponentMesh)source[MuTag.MeshFilter];

            HashSet<int> vertIndicesToKeep = [];

            for (int index = meshSource.Triangles.Length - 1; index >= 0; index--)
            {
               Int3 triangle = meshSource.Triangles[index];
               if (triangleIndices.Contains(index))
               {
                   List<Int3> list = meshSource.Triangles.ToList();
                   list.RemoveAt(index);
                   meshSource.Triangles = list.ToArray();
               }
               else
               {
                   vertIndicesToKeep.Add(triangle.X);
                   vertIndicesToKeep.Add(triangle.Y);
                   vertIndicesToKeep.Add(triangle.Z);
               }
            }

            int newIndex = 0;
            Dictionary<int, int> mapping = [];
            for (int index = 0; index < meshSource.VertexData.Length; index++)
            {
                if (vertIndicesToKeep.Contains(index))
                {
                    mapping[index] = newIndex;
                    newIndex++;
                }
            }

            for (int index = meshSource.VertexData.Length - 1; index >= 0; index--)
            {
                if (!vertIndicesToKeep.Contains(index))
                {
                    List<VertexData> list = meshSource.VertexData.ToList();
                    list.RemoveAt(index);
                    meshSource.VertexData = list.ToArray();
                }
            }

            for (int triangleIndex = 0; triangleIndex < meshSource.Triangles.Length; triangleIndex++)
            {
                Int3 triangleCurrent = meshSource.Triangles[triangleIndex];
                meshSource.Triangles[triangleIndex] = new Int3(
                    mapping[triangleCurrent.X],
                    mapping[triangleCurrent.Y],
                    mapping[triangleCurrent.Z]);
            }
        }
    }
}