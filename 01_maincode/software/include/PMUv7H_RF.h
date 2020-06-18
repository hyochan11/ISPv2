//************************************************************
// Desciption: PMUv7H Register File Header File
//      Generated by genRF 05/07/2017 22:12:07
//************************************************************

#ifndef PMUV7H_RF_H
#define PMUV7H_RF_H

// Register 0x00
// -- READ-ONLY --

// Register 0x01
// -- EMPTY --

// Register 0x02
// -- EMPTY --

// Register 0x03
// -- EMPTY --

// Register 0x04
// -- EMPTY --

// Register 0x05
// -- EMPTY --

// Register 0x06
// -- EMPTY --

// Register 0x07
// -- EMPTY --

// Register 0x08
// -- EMPTY --

// Register 0x09
// -- EMPTY --

// Register 0x0A
// -- EMPTY --

// Register 0x0B
// -- EMPTY --

// Register 0x0C
// -- EMPTY --

// Register 0x0D
// -- EMPTY --

// Register 0x0E
// -- EMPTY --

// Register 0x0F
// -- EMPTY --

// Register 0x10
// -- EMPTY --

// Register 0x11
// -- EMPTY --

// Register 0x12
// -- EMPTY --

// Register 0x13
// -- EMPTY --

// Register 0x14
// -- EMPTY --

// Register 0x15
// -- EMPTY --

// Register 0x16
// -- EMPTY --

// Register 0x17
// -- EMPTY --

// Register 0x18
// -- EMPTY --

// Register 0x19
// -- EMPTY --

// Register 0x1A
// -- EMPTY --

// Register 0x1B
// -- EMPTY --

// Register 0x1C
// -- EMPTY --

// Register 0x1D
// -- EMPTY --

// Register 0x1E
// -- EMPTY --

// Register 0x1F
// -- EMPTY --

// Register 0x20
// -- EMPTY --

// Register 0x21
// -- EMPTY --

// Register 0x22
// -- EMPTY --

// Register 0x23
// -- EMPTY --

// Register 0x24
// -- EMPTY --

// Register 0x25
// -- EMPTY --

// Register 0x26
// -- EMPTY --

// Register 0x27
// -- EMPTY --

// Register 0x28
// -- EMPTY --

// Register 0x29
// -- EMPTY --

// Register 0x2A
// -- EMPTY --

// Register 0x2B
// -- EMPTY --

// Register 0x2C
// -- EMPTY --

// Register 0x2D
// -- EMPTY --

// Register 0x2E
// -- EMPTY --

// Register 0x2F
// -- EMPTY --

// Register 0x30
// -- EMPTY --

// Register 0x31
// -- EMPTY --

// Register 0x32
// -- EMPTY --

// Register 0x33
// -- EMPTY --

// Register 0x34
// -- EMPTY --

// Register 0x35
// -- EMPTY --

// Register 0x36
// -- EMPTY --

// Register 0x37
// -- EMPTY --

// Register 0x38
// -- EMPTY --

// Register 0x39
// -- EMPTY --

// Register 0x3A
// -- EMPTY --

// Register 0x3B
// -- EMPTY --

// Register 0x3C
// -- EMPTY --

// Register 0x3D
// -- EMPTY --

// Register 0x3E
// -- EMPTY --

// Register 0x3F
// -- EMPTY --

// Register 0x40
// -- EMPTY --

// Register 0x41
// -- EMPTY --

// Register 0x42
// -- EMPTY --

// Register 0x43
// -- EMPTY --

// Register 0x44
// -- EMPTY --

// Register 0x45
// -- EMPTY --

// Register 0x46
// -- EMPTY --

// Register 0x47
// -- EMPTY --

// Register 0x48
// -- EMPTY --

// Register 0x49
// -- EMPTY --

// Register 0x4A
// -- READ-ONLY --

// Register 0x4B
// -- READ-ONLY --

// Register 0x4C
// -- READ-ONLY --

// Register 0x4D
// -- READ-ONLY --

// Register 0x4E
// -- READ-ONLY --

// Register 0x4F
// -- READ-ONLY --

// Register 0x50
// -- READ-ONLY --

// Register 0x51
typedef union pmuv7h_r51{
  struct{
    unsigned LC_CLK_RING		: 2;
    unsigned LC_CLK_DIV		: 2;
    unsigned PMU_IRQ_EN		: 1;
    unsigned PMU_CHECK_WRITE		: 1;
    unsigned EN_GLITCH_FILT		: 1;
  };
  uint32_t as_int;
} pmuv7h_r51_t;
#define PMUv7H_R51_DEFAULT {{0x1, 0x3, 0x1, 0x0, 0x0}}
_Static_assert(sizeof(pmuv7h_r51_t) == 4, "Punned Structure Size");

// Register 0x52
typedef union pmuv7h_r52{
  struct{
    unsigned INT_RPLY_REG_ADDR		: 8;
    unsigned INT_RPLY_SHORT_ADDR		: 8;
  };
  uint32_t as_int;
} pmuv7h_r52_t;
#define PMUv7H_R52_DEFAULT {{0x00, 0x10}}
_Static_assert(sizeof(pmuv7h_r52_t) == 4, "Punned Structure Size");

// Register 0x53
// -- READ-ONLY --

#endif // PMUV7H_RF_H