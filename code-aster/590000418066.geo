// Gmsh project created on Thu Apr 23 10:16:03 2026
SetFactory("OpenCASCADE");
cl1 = 100;
Point(1) = {0,-1000,0, cl1};
Point(2) = {0,-1000,1000, cl1};
Point(3) = {0,-500,1000, cl1};
Point(4) = {0,0,1000, cl1};
//+
Line(1) = {2, 1};
//+
Line(2) = {2, 3};
//+
Line(3) = {3, 4};
//+
Symmetry {0, 1, 0, 0} {
  Duplicata { Curve{3}; Curve{2}; Curve{1}; }
}
//+ MAX CHARS IN GROUP NAME = 24
Physical Curve("topbeam") = {2, 3, 4, 5}; 
//+
Physical Curve("mast") = {6};
Physical Point("groundS") = {1};
//+
Physical Point("groundN") = {12};
//+
Physical Point("massN") = {9};
Physical Point("loadS") = {3};
