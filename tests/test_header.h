/*
license block
*/

#ifndef TYPICAL_INCLUDE_GUARD_H
#define TYPICAL_INCLUDE_GUARD_H

//
// Includes
#include <stdlib.h>

//
// Defines
#define DEFAULT_NOMS (8)

//
// Type Definitions
typedef struct _my_struct_t {
    uint8_t console;
} shorty_base_t;

typedef enum {
    ENUM_VAL_0 = 0,
    ENUM_VAL_1,
    ENUM_VAL_2,
    ENUM_VAL_3,
    ENUM_VAL_4,

    // number of enum values
    ENUM_VAL_NUM
} long_enum_e;

//
// Class Declaration
class ChildishClassbino : public Momma, protected Pops {
private:
    uint8_t _nominations = DEFAULT_NOMS; // private member

protected:
    uint32_t _dreams = 9001;

public:
    ChildishClassbino(void);
    ChildishClassbino(uint8_t oscars);

    void high_five( void ); // public member function

    void* waypoint = NULL; // public member

}

extern ChildishClassbino maiBino; // extern class

//
// Extern declarations
extern const uint8_t mysterious_var;

//
// Function declarations
void c_function( void );



#endif // TYPICAL_INCLUDE_GUARD_H