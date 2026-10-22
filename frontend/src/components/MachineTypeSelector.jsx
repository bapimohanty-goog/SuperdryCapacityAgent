import React, { useMemo } from 'react'
import {
  Box, TextField, MenuItem, Chip, Typography, ToggleButton,
  ToggleButtonGroup, Tooltip, Autocomplete,
} from '@mui/material'
import MemoryIcon from '@mui/icons-material/Memory'
import DeveloperBoardIcon from '@mui/icons-material/DeveloperBoard'
import ComputerIcon from '@mui/icons-material/Computer'
import SpeedIcon from '@mui/icons-material/Speed'
import StorageIcon from '@mui/icons-material/Storage'
import DnsIcon from '@mui/icons-material/Dns'
import TuneIcon from '@mui/icons-material/Tune'

const COMPUTE_CATEGORIES = [
  { value: 'GPU', label: 'GPU', icon: <MemoryIcon sx={{ fontSize: 15 }} /> },
  { value: 'TPU', label: 'TPU', icon: <DeveloperBoardIcon sx={{ fontSize: 15 }} /> },
  { value: 'General Purpose', label: 'General Purpose', icon: <ComputerIcon sx={{ fontSize: 15 }} /> },
  { value: 'Compute-Optimized', label: 'Compute-Optimized', icon: <SpeedIcon sx={{ fontSize: 15 }} /> },
  { value: 'Memory-Optimized', label: 'Memory-Optimized', icon: <DnsIcon sx={{ fontSize: 15 }} /> },
  { value: 'Storage-Optimized', label: 'Storage-Optimized', icon: <StorageIcon sx={{ fontSize: 15 }} /> },
  { value: 'Custom', label: 'Search / Custom', icon: <TuneIcon sx={{ fontSize: 15 }} /> },
]

/**
 * Multi-step machine type selector supporting all GCP compute types:
 * 1. Compute Category (GPU, TPU, General Purpose, Compute-Optimized, Memory-Optimized, Storage-Optimized, Custom)
 * 2. Chip / Machine Series (dropdown)
 * 3. VM Configuration (dropdown or free-solo search/custom input)
 */
export default function MachineTypeSelector({
  machineTypes = [],
  category, setCategory,
  chip, setChip,
  machineType, setMachineType,
  disabled = false,
  size = 'small',
}) {
  const isCpuCategory = ['General Purpose', 'Compute-Optimized', 'Memory-Optimized', 'Storage-Optimized'].includes(category)
  const isCustomCategory = category === 'Custom'

  // Group by chip / series for the selected category
  const chipGroups = useMemo(() => {
    const groups = {}
    machineTypes.forEach(mt => {
      const c = mt.chip || mt.gpu
      const cat = mt.category || 'GPU'
      if (cat !== category) return
      if (!groups[c]) {
        groups[c] = { chip: c, gpu: mt.gpu, types: [] }
      }
      groups[c].types.push(mt)
    })
    return groups
  }, [machineTypes, category])

  const chipList = useMemo(() => Object.values(chipGroups), [chipGroups])

  const selectedChipGroup = useMemo(() => chipGroups[chip] || null, [chipGroups, chip])

  const filteredMachineTypes = useMemo(() => {
    if (!selectedChipGroup) return []
    return selectedChipGroup.types
  }, [selectedChipGroup])

  const selectedMachineInfo = useMemo(() => {
    return machineTypes.find(mt => mt.machineType === machineType)
  }, [machineType, machineTypes])

  const allMachineTypeNames = useMemo(() => {
    return machineTypes.map(mt => mt.machineType)
  }, [machineTypes])

  const step2Label = category === 'GPU'
    ? 'GPU Chip'
    : category === 'TPU'
      ? 'TPU Version'
      : 'Machine Series'

  const getVmConfigHelperText = () => {
    if (!selectedMachineInfo) {
      if (isCustomCategory) {
        return machineType
          ? `Custom GCE machine type: ${machineType}`
          : 'Search any preset or enter a custom GCE type (e.g. n2-custom-8-32768)'
      }
      return chip ? 'Select a configuration' : `Select ${step2Label.toLowerCase()} first`
    }
    if (selectedMachineInfo.category === 'TPU') {
      return `${selectedMachineInfo.gpuCount} chip(s) · ${selectedMachineInfo.vcpus || '?'} vCPUs · ${selectedMachineInfo.hbmGb || '?'} GB HBM`
    }
    if (selectedMachineInfo.category === 'GPU') {
      return `${selectedMachineInfo.gpu} × ${selectedMachineInfo.gpuCount}`
    }
    return `${selectedMachineInfo.vcpus || '?'} vCPUs · ${selectedMachineInfo.memoryGb || '?'} GB RAM (${selectedMachineInfo.gpu})`
  }

  const getSummaryLabel = () => {
    if (!selectedMachineInfo) {
      return `${machineType} (Custom GCE)`
    }
    if (selectedMachineInfo.category === 'GPU') {
      return `${selectedMachineInfo.chip} × ${selectedMachineInfo.gpuCount} | ${selectedMachineInfo.zones?.length || 0} zones`
    }
    if (selectedMachineInfo.category === 'TPU') {
      return `${selectedMachineInfo.chip} (${selectedMachineInfo.gpuCount} chips) | ${selectedMachineInfo.zones?.length || 0} zones`
    }
    return `${selectedMachineInfo.vcpus} vCPUs · ${selectedMachineInfo.memoryGb} GB | ${selectedMachineInfo.zones?.length || 0} zones`
  }

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
      {/* Step 1: Compute Category */}
      <Box>
        <Typography variant="caption" color="text.secondary" sx={{ mb: 0.5, display: 'block', fontSize: '0.7rem' }}>
          Compute Category
        </Typography>
        <ToggleButtonGroup
          value={category}
          exclusive
          onChange={(_, val) => {
            if (val) {
              setCategory(val)
              setChip('')
              setMachineType('')
            }
          }}
          size="small"
          disabled={disabled}
          sx={{ flexWrap: 'wrap', gap: 0.5 }}
        >
          {COMPUTE_CATEGORIES.map(cat => (
            <ToggleButton
              key={cat.value}
              value={cat.value}
              sx={{
                px: 1.5, py: 0.6, textTransform: 'none', fontWeight: 500, gap: 0.5,
                fontSize: '0.78rem', borderRadius: '6px !important',
                border: '1px solid rgba(0, 0, 0, 0.12) !important',
              }}
            >
              {cat.icon} {cat.label}
            </ToggleButton>
          ))}
        </ToggleButtonGroup>
      </Box>

      {/* Step 2 & Step 3 */}
      <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap', alignItems: 'flex-end' }}>
        {!isCustomCategory && (
          <Box sx={{ minWidth: 220 }}>
            <TextField
              fullWidth
              select
              label={step2Label}
              value={chip}
              onChange={(e) => {
                setChip(e.target.value)
                setMachineType('')
              }}
              size={size}
              disabled={disabled}
              helperText={selectedChipGroup ? `${selectedChipGroup.gpu} (${selectedChipGroup.types.length} configs)` : `Select ${step2Label.toLowerCase()}`}
            >
              {chipList.map(cg => (
                <MenuItem key={cg.chip} value={cg.chip}>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, width: '100%', justifyContent: 'space-between' }}>
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                      <Chip
                        label={cg.chip}
                        size="small"
                        sx={{
                          bgcolor: '#e8f0fe', color: '#1a73e8', fontWeight: 600,
                          height: 22, fontSize: '0.7rem',
                        }}
                      />
                      {isCpuCategory && (
                        <Typography variant="caption" color="text.secondary" sx={{ fontSize: '0.7rem' }}>
                          {cg.gpu}
                        </Typography>
                      )}
                    </Box>
                    <Typography variant="body2" color="text.secondary" sx={{ fontSize: '0.72rem', ml: 1 }}>
                      {cg.types.length} config{cg.types.length > 1 ? 's' : ''}
                    </Typography>
                  </Box>
                </MenuItem>
              ))}
            </TextField>
          </Box>
        )}

        {/* Step 3: VM Configuration or Custom Input */}
        {isCustomCategory ? (
          <Box sx={{ minWidth: 340, flexGrow: 1, maxWidth: 520 }}>
            <Autocomplete
              freeSolo
              options={allMachineTypeNames}
              value={machineType}
              onChange={(_, newVal) => setMachineType((newVal || '').trim())}
              onInputChange={(_, newInput) => setMachineType((newInput || '').trim())}
              disabled={disabled}
              size={size}
              renderOption={(props, option) => {
                const info = machineTypes.find(m => m.machineType === option)
                return (
                  <li {...props} key={option}>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', width: '100%', alignItems: 'center', gap: 1 }}>
                      <Box>
                        <Typography variant="body2" sx={{ fontWeight: 500 }}>{option}</Typography>
                        {info && (
                          <Typography variant="caption" color="text.secondary" sx={{ fontSize: '0.68rem' }}>
                            {info.category} · {info.family} · {info.vcpus ? `${info.vcpus} vCPUs, ${info.memoryGb} GB` : info.gpu}
                          </Typography>
                        )}
                      </Box>
                      {info && (
                        <Chip label={info.category} size="small" sx={{ height: 20, fontSize: '0.65rem' }} />
                      )}
                    </Box>
                  </li>
                )
              }}
              renderInput={(params) => (
                <TextField
                  {...params}
                  label="Machine Type (Search or Custom)"
                  placeholder="e.g. c4-standard-8, n2-custom-8-32768, a3-highgpu-8g"
                  helperText={getVmConfigHelperText()}
                />
              )}
            />
          </Box>
        ) : (
          <Box sx={{ minWidth: 260 }}>
            <TextField
              fullWidth
              select
              label="VM Configuration"
              value={machineType}
              onChange={(e) => setMachineType(e.target.value)}
              size={size}
              disabled={disabled || !chip}
              helperText={getVmConfigHelperText()}
            >
              {filteredMachineTypes.map(mt => (
                <MenuItem key={mt.machineType} value={mt.machineType}>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', width: '100%', alignItems: 'center', gap: 1 }}>
                    <Box>
                      <Typography variant="body2" sx={{ fontWeight: 500, lineHeight: 1.2 }}>
                        {mt.machineType}
                      </Typography>
                      <Typography variant="caption" color="text.secondary" sx={{ fontSize: '0.65rem' }}>
                        {mt.category === 'TPU'
                          ? `${mt.gpuCount} chips · ${mt.vcpus || '?'} vCPUs · ${mt.memoryGb || '?'} GB RAM · ${mt.hbmGb || '?'} GB HBM`
                          : mt.category === 'GPU'
                            ? mt.family
                            : `${mt.vcpus || '?'} vCPUs · ${mt.memoryGb || '?'} GB RAM`}
                      </Typography>
                    </Box>
                    <Chip
                      label={
                        mt.category === 'TPU'
                          ? `${mt.gpuCount} chips`
                          : mt.category === 'GPU'
                            ? `${mt.gpuCount}× ${mt.chip || ''}`
                            : `${mt.vcpus} vCPU / ${mt.memoryGb} GB`
                      }
                      size="small"
                      sx={{ height: 22, fontSize: '0.65rem', fontWeight: 600 }}
                    />
                  </Box>
                </MenuItem>
              ))}
            </TextField>
          </Box>
        )}

        {/* Selected info chip */}
        {machineType && (
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5, pb: '20px' }}>
            <Tooltip title={selectedMachineInfo ? `${selectedMachineInfo.gpu} — ${selectedMachineInfo.zones?.length || 0} zones available` : `Custom machine type: ${machineType}`}>
              <Chip
                icon={<MemoryIcon sx={{ fontSize: 14 }} />}
                label={getSummaryLabel()}
                size="small"
                variant="outlined"
                color="primary"
                sx={{ height: 26, fontSize: '0.72rem', fontWeight: 500 }}
              />
            </Tooltip>
          </Box>
        )}
      </Box>
    </Box>
  )
}
