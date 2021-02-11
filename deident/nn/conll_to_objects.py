def conll_to_objects(conll):
    previous_token_label = 'O'
    text = ''
    entity_id = 1
    entities = []
    entity = {}
    for line in conll.splitlines():
        line = line.strip().split(' ')
        # New sentence
        if len(line) == 0 or len(line[0]) == 0 or '-DOCSTART-' in line[0]:
            # Add the last entity 
            if entity != {}:
                entities.append(entity)
                entity_id += 1
                entity = {}
            previous_token_label = 'O'
            continue
        
        label = str(line[-1]).replace('_', '-') # For LOCATION-OTHER
        if label == 'O':
            # Previous entity ended
            if previous_token_label != 'O':
                entities.append(entity)
                entity_id += 1
                entity = {}
            previous_token_label = 'O'
            continue
        
        token = {}
        token['text'] = str(line[0])
        token['start'] = int(line[2])
        token['end'] = int(line[3])
        token['label'] = label[2:]
    
        if label[:2] == 'B-':
            if previous_token_label != 'O':
                # End the previous entity
                entities.append(entity)
                entity_id += 1
            # Start a new entity
            entity = token
        elif label[:2] == 'I-':
            # Entity continued
            if previous_token_label == token['label']:
                # if there is no newline between the entity and the token
                if '\n' not in text[entity['end']:token['start']]:
                    # Update entity 
                    entity['text'] = entity['text'] + ' ' + token['text']
                    entity['end'] = token['end']
                else: # newline between the entity and the token
                    # End the previous entity
                    entities.append(entity)
                    entity_id += 1
                    # Start a new entity
                    entity = token
            elif previous_token_label != 'O':
                # End the previous entity
                entities.append(entity)
                entity_id += 1
                # Start new entity
                entity = token
            else: # previous_token_label == 'O'
                # Start new entity
                entity = token
        previous_token_label = token['label']
    
    if entity != {} and entity not in entities:
        entities.append(entity)
    
    return entities