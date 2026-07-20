def format_pubsub_response(res):                                                                                                                                                               
    if res is None:                                                                                                                                                                            
        return "(nil)"                                                                                                                                                                         
    if isinstance(res, str) and (res.startswith("WRONGTYPE") or res.startswith("ERR")):                                                                                                        
        return res                                                                                                                                                                             
    if isinstance(res, int):                                                                                                                                                                   
        return f"(integer) {res}"                                                                                                                                                              
    if isinstance(res, list):                                                                                                                                                                  
        # Format subscription confirmation messages                                                                                                                                            
        lines = []                                                                                                                                                                             
        for item in res:                                                                                                                                                                       
            if isinstance(item, list):                                                                                                                                                         
                for i, val in enumerate(item, 1):                                                                                                                                              
                    lines.append(f"{i}) {val}")                                                                                                                                                
            else:                                                                                                                                                                              
                lines.append(str(item))                                                                                                                                                        
        return "\n".join(lines)                                                                                                                                                                
    return str(res)                                                                                                                                                                            
                                                                                                                                                                                                
def subscribe_command(db, client_socket, args):                                                                                                                                                
    if len(args) < 1:                                                                                                                                                                          
        return "ERR - wrong number of args"                                                                                                                                                    
    channels = args                                                                                                                                                                            
    res = db.subscribe(client_socket, *channels)                                                                                                                                               
    return format_pubsub_response(res)                                                                                                                                                         
                                                                                                                                                                                                
def unsubscribe_command(db, client_socket, args):                                                                                                                                              
    channels = args                                                                                                                                                                            
    res = db.unsubscribe(client_socket, *channels)                                                                                                                                             
    return format_pubsub_response(res)                                                                                                                                                         
                                                                                                                                                                                                
def publish_command(db, args):                                                                                                                                                                 
    if len(args) != 2:                                                                                                                                                                         
        return "ERR - wrong number of args"                                                                                                                                                    
    channel = args[0]                                                                                                                                                                          
    message = args[1]                                                                                                                                                                          
    res = db.publish(channel, message)                                                                                                                                                         
    return format_pubsub_response(res)