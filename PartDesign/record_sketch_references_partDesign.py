
import lib_repair_sketch_references_partDesign
from lib_repair_sketch_references_partDesign import *

reference_state = [] #list instead of dictionary to preserve order.

for obj in FreeCAD.ActiveDocument.Objects:
    if obj.TypeId == 'Sketcher::SketchObject':
        if obj.ExternalGeometry != [] or obj.Support != None:
            debugPrint(3, 'parsing ShapeElementReferences from %s' % obj.Name )
            exGeom = []
            for se_obj,se in obj.ExternalGeometry:
                #try:
                exGeom.append( SketchReference(se_obj, se) )
                #except RuntimeError, msg:
                #    FreeCAD.Console.PrintError('unable to record %s.%s (%s), reference will be removed on update!\n' % ( se_obj.Name, se, str(msg) ) )
            if obj.Support != None:
                assert len( obj.Support[1] ) == 1
                supportGeom = SketchSupportReference( obj )
            else:
                supportGeom = None
            reference_state.append( [ obj.Name, exGeom, supportGeom ] )
    elif obj.TypeId == 'PartDesign::LinearPattern':
        refObj, refElements = obj.Direction
        if not refObj.TypeId == 'Sketcher::SketchObject' and len(refElements) == 1:
            debugPrint(3, 'parsing ShapeElementReferences from %s' % obj.Name )
            directionRef = DirectionReference( refObj, refElements[0] )
            reference_state.append( [ obj.Name, None, directionRef ] )
    elif  obj.TypeId in ['PartDesign::Fillet', 'PartDesign::Chamfer']:
        refObj, refElements = obj.Base
        debugPrint(3, 'parsing ShapeElementReferences from %s' % obj.Name )
        edgeReferences = [ EdgeReference( refObj, r) for r in refElements ]
        reference_state.append( [ obj.Name, edgeReferences, None ] )

lib_repair_sketch_references_partDesign.reference_state = reference_state
debugPrint( 1, 'Sketch references recorded', timePrefix=True )
