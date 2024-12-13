import grpc
import pb.properties_pb2
import pb.properties_pb2_grpc

def run():
    # Connect to the server
    with grpc.insecure_channel('localhost:50052') as channel:
        stub = pb.properties_pb2_grpc.PropertyServiceStub(channel)
        
        # Create a request
        request = pb.properties_pb2.FilterPropertyRequest(
            # The line `# area={"min": 50, "max": 100},` is a commented-out line in the code snippet
            # you provided. This means that it is not currently being executed by the program.
            area={"min": 50, "max": 100},
            page=1,
        )
        
        # Make the call
        response = stub.SearchProperties(request)
        
        # Print the response
        print("SearchProperties response received")
        
        response = stub.CountProperties(request)
        print("CountProperties response received", response)
        
        request = pb.properties_pb2.SinglePropertyRequest(property_id_nma="0301-148-303-0-0")
        response = stub.GetProperty(request)
        print("GetProperty response received")
        
        request = pb.properties_pb2.PropertyUnitsRequest(property_id_nma="0301-148-303-0-0", page=1)
        response = stub.GetPropertyUnits(request)
        print("GetPropertyUnits response received")
        
        response = stub.CountPropertyUnits(request)
        print("CountPropertyUnits response received", response)
        
        request = pb.properties_pb2.SingleUnitRequest(unit_id=288292015)
        response = stub.GetUnit(request)
        print("GetUnit response received")
        
        request = pb.properties_pb2.OwnedItemsRequest(owner_id="40008146", page=1)
        response = stub.GetOwnedProperties(request)
        print("GetOwnedProperties response received")
        
        response = stub.CountOwnedProperties(request)
        print("CountOwnedProperties response received", response)

if __name__ == "__main__":
    run()
